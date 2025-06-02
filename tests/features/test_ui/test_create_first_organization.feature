Feature: Create First Organization

  @ui
  Scenario: Create first organization
    Given I am on the welcome new user page
    When I press the let's do it button
    Then I should be redirected to the join organization page

    When I press create organization button
    Then I should be redirected to the name your organization page

    When I type "My-new-organization" to the input filed
    And I press next button
    Then I should be redirected to the that's it page

    When I press the let's do it button
    Then I should be redirected to the dashboard
    And project creation message for "My-new-organization" is displayed
    And create project button is displayed
