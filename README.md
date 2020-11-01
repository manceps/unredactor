# Unredactor

[Unredactor](https://www.manceps.com/projects/unredactor) is an app that allows you to replace any word with an `unk` then predict the masked word(s). It is easily launched by running a Docker container.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


### Installing

* Install the latest version of [Docker](https://docs.docker.com/get-docker/).
* Install [curl](https://curl.haxx.se/download.html) for you OS.
* Build the Docker container image.
  ```
  # Navigate to base directory.
  $ cd private-experiments
  
  # Build Docker container from Dockerfile
  $ docker build -t unredactor .
  ```
* Run newly built Unredactor image  
  `$ docker run unredactor`
  
* Send a request to the Unredactor service using curl.  
  + Example:  
  `$ curl -H "Content-Type: application/json" -d '{"text": "to unk or not to unk, that is the unk."}' http://localhost:8080/unredact` 

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Docker](https://docs.docker.com/) - Platform to create, deploy, and run containers.
* [Huggingface](https://huggingface.co/transformers/) - General purpose architectures for Natural Language Understanding (NLU) and Natural Language Generation (NLG).

## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Chris Thompson, Hobson Lane** and the Manceps Summer Interns for their contribution to the original Unredactor.  

  ### Interns:  

  - Hope Yim
  - Tyler Gee
  - Julian McOmie
  - Alex Kari
