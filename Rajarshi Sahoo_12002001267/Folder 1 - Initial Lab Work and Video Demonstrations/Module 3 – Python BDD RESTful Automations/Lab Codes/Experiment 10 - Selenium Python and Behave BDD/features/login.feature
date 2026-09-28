Feature: SauceDemo Login

  Scenario: Successful login with valid credentials
    Given the user opens the SauceDemo website
    When the user enters valid username and password
    And the user clicks the login button
    Then the user should be redirected to the products page