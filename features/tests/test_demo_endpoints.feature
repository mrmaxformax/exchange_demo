# Created by mterekhov at 4/2/22
Feature: Test Demo Endpoints

  Scenario: Validate the Open Orders response
    Given Lets work with demo API
    When get Demo Open Orders Value
    Then validate Demo Open Orders Value