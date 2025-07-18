# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    discount = 0.9
    iterations = 100
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        count = 0
        while count < self.iterations:
            val = util.Counter() #val noi calculate pt stari

            for i in self.mdp.getStates(): #parcurg stari mdp
                if not self.mdp.isTerminal(i):
                    max_val = -99999999
                    for j in self.mdp.getPossibleActions(i): #parcurg actiuni
                        q_val = self.computeQValueFromValues(i, j)
                        max_val = max(max_val, q_val)
                    val[i] = max_val
                else:
                    val[i] = 0 #stare terminala
            count = count + 1
            self.values = val

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
                  Compute the Q-value of action in state from the
                  value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q = 0
        tranzitii = self.mdp.getTransitionStatesAndProbs(state, action)

        for i, j in tranzitii: #i stare urmatoare, j probabilitate
            recompensa = self.mdp.getReward(state, action, i)
            factor_reducere = self.values[i] * self.discount
            q += j * (factor_reducere + recompensa)

        return q

    def computeActionFromValues(self, state):
        """
                  The policy is the best action in the given state
                  according to the values currently stored in self.values.

                  You may break ties any way you see fit.  Note that if
                  there are no legal actions, which is the case at the
                  terminal state, you should return None.
         """
        "*** YOUR CODE HERE ***"
        actiune = None
        val = -99999999

        if self.mdp.isTerminal(state):
            return None
        else:
         for i in self.mdp.getPossibleActions(state):
             q = self.computeQValueFromValues(state, i)
             if q > val:
                 val = q
                 actiune = i

        return actiune

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self): #q4
        "*** YOUR CODE HERE ***"