Feature: SauceDemo Login using Page Object Model

  Scenario: Successful login using valid credentials
    Given the user opens the SauceDemo website
    When the user enters valid login credentials
    And the user clicks the login button
    Then the user should be redirected to the products page