#!/usr/bin/env bash

# Run all unit tests with coverage report
coverage erase
coverage report -m "--include=*/tal-locust/*"
