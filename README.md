# Pygrator

The main idea of this project is to ease the problems faced whilst migrating data into databases.

To keep it simple, it supports only Postgres.

## Current progress

Not stable - still building basic structure.

## What to expect

Given a set of models, it should keep tables' structure consistent. In other words, it must make sure it can create tables, add and remove columns, delete tables and change column type.

All of them should keep state of previous operation, thus creating historical data of database manipulation.