Introduction
=====

Author: Clayton Henderson

Purpose
-----

Luna stands for Lexical Universal Natural Assistant.   The goal of this project is
to make it easier to work with technology, handle tedious tasks, and get general help
with anything able to be helped.  In the end the idea is that this will be an always
on application running on multiple devices, synchronizing and communicating in real time,
to accomplish tasks such as home automation, general secretarial duties, monitor vitals, 
display anything from one device on another device, utilize hardware from one device on
another, and a monsterous amount of other things.

Background
-----

The inspiration for this project came from Jarvis from Iron Man and 
the strong desire to automate as many tasks as possible to free up
our own time to do the things we love.

NOTE 1 All code and documentation is liable to drastically change at any point in these early stages.  This disclaimer will be removed once the project has become more stable.  Please still feel free to git the code and test anything in it's current state!  All current code is 100% prototype code and is in no way meant to reflect the final outcome.  Please keep this in mind when working with, on, or reviewing the code. Enjoy!

NOTE 2 I would like to start by reminding the reader what the end goal of this project means in terms of how this project is being designed and modeled.  This system is meant to control any device and to be able to do so with the confidence of a users verbal command.  These things can sometimes be 100% autonomous and require no actual true input from the user but from what the system interpreted from the dialogue and/or situation the user is currently in.  Other times it will be a direct command from the user verbally, app, website, command line, and if we're gonna go really crazy, it would be fun for it to be able to communicate using notepad if nothing else is available.  Obviously these are all end goals for the project and it's current state is an extremely early base prototype of a prototype of a prototype and so on, but it helps to think of the larger picture when designing early on to work out as many kinks as we can while we're here but without dragging the project out too long. 

High Level Breakdown
=====

Concept
------
 * The concept here is to have an "entity" that can control a system and act as a digital assistant for those devices and the services they provide.
 * Since this concept is to have a digital assistant whose primary means of interaction is spoken commands, it made sense to design it after a human from a top down perspective.
 * Designing after a human made sense for several reasons such as how the assistant is supposed to be able to listen in to conversations around it and be able to pull and interpret data from it however it helps from a design perspective because it allows me to keep a focus and naming convention going after something that is well established and rather relatable.
 * It is worth noting that it is early enough in the project still that any new design ideas won't go unheard.

Brain
-----
 * Central system that runs on the primary service.  It handles managing all the other systems.
 * Handles processing using cortices, specialized objects designed to handle the primary processing of the system.
 * Spawns subproccesses

Nervous System
-----
 * Manager of communication across the entire system.  This is actually a library that will be used by all the other systems.
 * The Brain is where the primary "Central" nervous system will be located that will keep track of all the current neurons and pathways.
 * This is basically a wrapper around Redis.  Redis acts very much like a central nervous system would for a body, hence the name of the module for Luna.
 * I will come up with protocols for the messages that will travel on the pipelines so that data isn't haphazardly tossed into channels and have wasted processing time later.  Anything using the nervous system needs to be as efficient and performant as possible without exception.  This is the backbone of the system seeing how the system is broken into several processes that must communicate.

Senses
------
 * All major pieces of the system that involve direct communication with the central nervous system.
 * Examples would be things like input from or output to any source such as audio, video, or text. 
  
Immune System
------
 * Manager of the over state and health of the system.
 * Monitors the other services to ensure integrity, performance, and operation.
 * Gathers logs
 * Spawns subproccesses
  
Extremeties
-----
 * All extraneous pieces of the system, such as plugins.


Structure
======

Design
-----
The system will run in several different pieces that will all have to communicate while running independently.  Originally I was going to have a process manager that would handle a separate process spun for each item that needed it and would handle managing those processes manually.  However after speaking with my brother he mentioned instead separating out the processes into their own services and have the operating system handle them.  That way the operating system handles keeping the important pieces running that need to always be running.  With this in mind the important pieces that need to run separately will do so as their own service and use redis, hereby referred to as the central nervous system, for communication.

Services
-----
 * Brain
 * Ears
 * Mouth
 * Eyes
 * Extremeties
 * ImmuneSystem

 Installation
 ------

Overview
------
Being what this is supposed to be in the end, I find it suiting that the application be able to install itself right off of the bat.  A single install file for each system is what we will start with for installation.  The file will pull the latest code from git and run the correct install file for the system being run on.  If able, the system will proceed to install all the items in the requirements file that are not already installed for the bare minimum install.  The system will then need to start and connect to the central nervous system.  If there is no system found it will proceed to assume this is the initial installation and continue to install all necessary requirements and setup all the rest of the services.  If the system starts for the first time and detects a central nervous system already in place then it will attempt to connect and register with the brain.  If successful then the brain will send all the configuration data needed for the new lobe based on the 

The install file will have to know the minimum requirements of Luna and be able to look at the system to determine if it's even possible to run it.  It will inform the user if it is unable to run and give the reasons why, as many as possible.  
