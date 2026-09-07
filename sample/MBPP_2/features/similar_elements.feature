Feature: Find similar elements between two tuples
  As a collection utility
  I want to retrieve the common elements from two tuple inputs
  So that I can identify overlapping data

  Scenario: Common elements are 4 and 5
    Given first tuple (3, 4, 5, 6)
    And second tuple (5, 7, 4, 10)
    When I compute similar elements
    Then the result should be (4, 5)

  Scenario: Common elements are 3 and 4
    Given first tuple (1, 2, 3, 4)
    And second tuple (5, 4, 3, 7)
    When I compute similar elements
    Then the result should be (3, 4)

  Scenario: Common elements are 13 and 14
    Given first tuple (11, 12, 14, 13)
    And second tuple (17, 15, 14, 13)
    When I compute similar elements
    Then the result should be (13, 14)

  Scenario: No common elements yields empty tuple
    Given first tuple (1, 2)
    And second tuple (3, 4)
    When I compute similar elements
    Then the result should be ()

  Scenario: Identical tuples return all elements
    Given first tuple (5, 6, 7)
    And second tuple (5, 6, 7)
    When I compute similar elements
    Then the result should be (5, 6, 7)