# PlagiarismDetection
This repository contains different activities regarding the Advanced Software Development module. The main goal of the module is to implement different technologies to develop a plagiarism detection software.

Inside the resources folder there are two folders that contain the original texts and the suspicious texts and a .json file that contains the Ground Truth.

The main code is inside the src folder with three folders. The algorithms folder contains the cosine algorithm script and the model script which is used to create the mediator and the alogrithms implemented.

Inside util there are scripts that help the software in general. config.py initialize the environment variables. file_manager.py contains different modules to manage files and directories under different operating systems. generator.py contains a set of classes that generate different useful data types for testing purposes. Finally, ioutils.py contains the module to manipulate the user's input and the module to load json files.

Inside wrapper there are two scripts, this scripts are used to run the software. demo.py, as the name says, runs a demonstration of the software. The run.py script creates the mediator, adds the Cosine algorithm and returns the comparison of the files from the directory given by the user.

## Docs

Document with the unit tests: https://docs.google.com/document/d/1r2pdu2DiKqYgYCbdfcz5XYGpE8EFZj0nr19AURX0cUY/edit?usp=sharing

Document that explains the functionality of the software: https://docs.google.com/document/d/1nUtJLPnNAoYO1EABDd77TsmZOzfbOkyBXR5RgnB2nyE/edit?usp=sharing

## Authors

Raúl Youthan Irigoyen Osorio A01750476@tec.mx

Eduardo Rodríguez López A01749381@tec.mx

Rebeca Rojas Pérez A01751192@tec.mx
