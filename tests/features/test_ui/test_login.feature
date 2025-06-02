Feature: Login Feature

  @ui
  Scenario: New user successful login
    Given I am on the login page
    When I enter valid credentials
    And I press the login button
    Then I should be redirected to the welcome new user page
