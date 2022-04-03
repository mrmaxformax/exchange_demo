# Created by mterekhov at 4/1/22

Feature: Test real API enpoints
  The tests for Server Time, Pairs and Open Order endpoints

  Background:
    Given Lets work with real API

  Scenario: Retrieve the server time, validate the response.
    When get server time
    Then validate server time response has equal values

  Scenario Outline: Retrieves XBT/USD trading pair, validates response.
    When get the asset pair info for "<pair>"
    Then validate the asset pair info for "<pair>"
    Examples:
      |   pair  |
      | XBT/USD |

  Scenario Outline: Retrieves XBT/USD trading pair, validates response.
    When get the asset pair info for "<pair>"
    Then validate the error for incorrect asset pair "<pair>"
    Examples:
      |   pair  |
      | AAA/BBB |

  Scenario: Validate the account does not have open orders
    When get Open Orders Value
    Then validate Open Orders Value is empty