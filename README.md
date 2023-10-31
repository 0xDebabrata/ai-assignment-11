# AI Assignment 11: Disease Prediction Expert System

**Name:** Debabrata Mondal<br/>
**Roll Number:** 002111001124<br/>

## Live Demo

**URL:** [Web GUI](https://ai-assignment-11.vercel.app/) <br/>
**Source code:** [GitHub](https://github.com/0xdebabrata/ai-assignment-11/)

## Abstract

This project includes an implementation for an expert system for medical 
disease diagnosis incorporating the following methodologies:

1. Rule-based systems
2. Knowledge-based systems
3. Database methodology
4. Inference engines
5. System-user interaction

It includes a web GUI where users are presented with a set of symptoms to 
choose from. The user can optionally select more symptoms. A limited set of 
diseases are supported at this time. The knowledge base inside a Prolog program
is used to find the matching set of diseases

## Project Description

The project includes two separate resources:
1. Web application
2. Server

The web application serves as the GUI for user interaction. All the processing 
is done at the server which is hosted on [Linode](https://linode.com). The 
Nextjs web application is hosted on [Vercel](https://vercel.com).

The server has access to a Prolog knowledge base and can execute queries 
against that. That is how it tries to match user-selected symptoms to 
diseases.

This project uses a bitmasking approach developed in collaboration with 
[Aditya Mayukh Som](https://github.com/adityamayukhsom) to generate a dynamic 
set of questions based on user's previous selections. 
Each symptom is assigned a number based on the number of diseases where it 
prevails. The mask of a disease is computed as the bitwise OR of the masks of
all the symptoms associated with that disease.

When the user selects their initial symptoms, these symptoms are converted 
into their respective masks and a new mask is created by computing the bitwise 
OR of all the selected symptoms. Bitwise AND operations are then performed 
with all diseases. If the result equals the newly created mask, additional 
questions about the other symptoms of that disease are presented. 
This approach creates a chain of questions that aids in precise disease 
prediction.

## Tech Stack

**Frontend:** Nextjs, TypeScript <br/>

**Backend:** Python, FastAPI, Prolog, FastAPI<br/>

## Attributions

This project uses a knowledge base derived from a publicly available Kaggle
dataset available at this link: [Kaggle Dataset Link](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset).
