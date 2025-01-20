Pour améliorer la scalabilité à long terme, on pourra :

    Dockeriser PostgreSQL pour isoler l’environnement.
    Configurer des migrations automatiques avec Django.
    Intégrer des solutions comme Amazon RDS pour un hébergement cloud scalable.


#All from Foodles
You joined Foodles and your first task is to design a brand new api to manage stocks and purchases.

## Instructions

This project is split in two steps, the problem should be tackled one step at a time, the second step relies on the first one.

You may read the whole project before starting to work on the first part.
You are expected to only focus on the backend part, you are not expected to create any front-end for this project.


## Expectations

For the first part, you are expected to write a working application. Code should have production ready quality.

For the second part you can continue on the application you just wrote. If you exhausted the time you decided to dedicate on this test you can explain the steps that you would take in order to achieve the desired outcome (be sure to be as precise as possible).

During the review we will go through what you have done so far. Depending on your steps completion, we may design and implement together steps not done yet. Be sure to have a working development environment by then.

You don't need to set up a CI/CD pipeline for the project.

You should focus on the database modelization part this will be the part on which you will be expected to present high quality work. Modelization is the part of the application which is the most difficult to change in the future so it's important to have a modelization as good as possible from the start.

## Project

1 - We need a new system to handle our stocks
Your task is to design a stock management system to handle our warehouse's operations.
We store products in locations in our warehouse.
- We want to be able to move products from one location to another and keep an history of each move that happened inside the warehouse.
- Each location can only contain one type of product at a given point in time, you cannot have both Coca Cola and Orange Juice at the same time in the same location.
- We want to be able to know what are the current stock level in each of our locations.

Write a web api that lets the warehouse operators move products from one location to another location.

You don't need to create an api to populate the warehouse or create the various objects you will use for this project,
you can use fixtures instead for instance.

2 - Let's start selling products
We will use one of our locations to sell products on our website, we'll call this location "website" for the rest of the exercise.
All products on this location will be available for purchase on our website.
Our client should be able to add products to their cart from the website location and then proceed to checkout.
Once in a cart a product should not be available for purchase to other customers.

We want to keep track of which items were purchased by each client and how much was paid by the customer.
During the checkout we should process a client payment by calling a third party api (POST https://external-provider.com/api/refund/ {â€œamountâ€: number, â€œclient_idâ€: number}).
The provider is an old company so their endpoints takes two minutes to answer on average.

