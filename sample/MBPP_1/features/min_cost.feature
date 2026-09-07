Feature: Minimum cost path in a cost matrix
  As an algorithmic utility
  I want to compute the minimum cost to reach a target cell (m, n) from (0, 0)
  So that I can determine the cheapest path through a grid

  Scenario: Minimum cost for first example matrix
    Given a cost matrix [[1, 2, 3], [4, 8, 2], [1, 5, 3]]
    And target row 2 and column 2
    When I compute the minimum cost
    Then the result should be 8

  Scenario: Minimum cost for second example matrix
    Given a cost matrix [[2, 3, 4], [5, 9, 3], [2, 6, 4]]
    And target row 2 and column 2
    When I compute the minimum cost
    Then the result should be 12

  Scenario: Minimum cost for third example matrix
    Given a cost matrix [[3, 4, 5], [6, 10, 4], [3, 7, 5]]
    And target row 2 and column 2
    When I compute the minimum cost
    Then the result should be 16

  Scenario: Target is the starting cell (0,0)
    Given a cost matrix [[1, 2, 3], [4, 8, 2], [1, 5, 3]]
    And target row 0 and column 0
    When I compute the minimum cost
    Then the result should be 1

  Scenario: Target is on the first row (0,2)
    Given a cost matrix [[1, 2, 3], [4, 8, 2], [1, 5, 3]]
    And target row 0 and column 2
    When I compute the minimum cost
    Then the result should be 6