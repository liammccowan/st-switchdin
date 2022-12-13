# SwitchDin ST

## Dependencies
- python3 (3.8.10 used for implementation)
- ansible (2.12.10 used for implementation) (for running on a remote host using playbook)
- paho-mqtt (1.6.1) (for running locally)
- docker (20.10.21) (for running locally)

## Running
Can be run locally, or using the provided ansible playbook to run on a remote server.

### Running Locally
Ensure dependencies are installed, excluding ansible.

Start a RabbitMQ message broker in a container:
- `docker run -d --hostname my-rabbit --name some-rabbit -p 1883:1883 rabbitmq:3`
- `docker exec some-rabbit rabbitmq-plugins enable rabbitmq_mqtt`
- `docker exec some-rabbit rabbitmqctl start_app`

Now run the python files found in `st`. It is recommended to run as follows:
- `python3 st/printer.py`
- `python3 st/receiver.py`
- `python3 st/generator.py`

Note that these files can be run in any order if desired, and `receiver.py` and `generator.py` can be run in the background.

### Using Ansible Playbook
In this case, only python3 and ansible need to be installed locally.
Note that a remote Ubuntu 22.04 server will need to be set up already.

Update the file `ansible/hosts` to include the information for the server that has already been set up.

Run `ansible-playbook playbook.yml -i ansible/hosts -1 st_aws_instance`. Replace `st_aws_instance` with the name of the server provided in the `ansible/hosts` file.

`ssh` into the remote server and run `python3 st/printer.py` to see the averages. `receiver.py` and `generator.py` are run in the playbook.

## Implementation
### `generator.py`
This contains the random number generator. It publishes a random number between 1 and 100 and a timestamp on a random interval between 1 and 30 seconds to an MQTT topic in the RabbitMQ message broker running in a container.

### `receiver.py`
This subscribes to the message from the generator, reads the number, and calculates 1 minute, 5 minute, and 30 minute averages. It uses the timestamp included in each message to keep track of if a particular value can be used in an average. Whenever a message is received, the averages are updated, and then published to another MQTT topic in the message broker.

### `printer.py`
This subscribes to the averages calculated by the receiver, and prints them as it receives them. As it only prints the averages, the printer can be stopped and started without affecting the averages.

## Notes
- This implementation uses pickle for serialization and deserialization of published payloads. Note that as pickle is python specific, it may be worth exploring alternatives if this system were to include components written in other languages.
- This is just a demo implementation, and as such some things are omitted for brevity. For example, there is minimal error checking, and some values are hardcoded (such as the connection settings). If this system were to be developed further, it would be valuable to improve these aspects.
- The data is lost one it is older than the largest average window (30 minutes). If this system were to be developed further, some way of storing the received data would be a useful addition.
- A graphical format to present the values over time would likely provide more clarity than the current tabular format used by the printer.