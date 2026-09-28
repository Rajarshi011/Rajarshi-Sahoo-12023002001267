Feature: Data-Driven SauceDemo Login

  Scenario: Login using multiple sets of test data
    Given the user opens the SauceDemo website
    When the user performs login tests using the CSV data
    Then all login test cases should produce the expected results