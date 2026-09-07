Feature: Detecting close numbers in a list
  As a data validation system
  I want to check whether any two numbers in a list are closer than a threshold
  So that I can flag lists with suspiciously similar values

  Scenario: No two numbers are within the threshold
    Given a list of numbers [1.0, 2.0, 3.0]
    When I check for close elements with threshold 0.5
    Then the result should be False

  Scenario: Two numbers are within the threshold
    Given a list of numbers [1.0, 2.8, 3.0, 4.0, 5.0, 2.0]
    When I check for close elements with threshold 0.3
    Then the result should be True

  Scenario: Single element list has no pairs to compare
    Given a list of numbers [1.0]
    When I check for close elements with threshold 0.1
    Then the result should be False

  Scenario: Duplicate values are closer than any positive threshold
    Given a list of numbers [1.0, 1.0]
    When I check for close elements with threshold 0.1
    Then the result should be True

  Scenario: Exact threshold boundary is not considered closer than threshold
    Given a list of numbers [1.0, 2.0]
    When I check for close elements with threshold 1.0
    Then the result should be False