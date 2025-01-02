import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def AI_cards(hand, current_deck, dealer_hand, reveal_dealer):
    # Calculate the current score of the AI and the dealer
    ai_score = calculate_score(hand)
    dealer_score = calculate_score(dealer_hand if reveal_dealer else dealer_hand[1:])
    
    # Fuzzy variables
    ai_score_lv = ctrl.Antecedent(np.arange(0, 32, 1), 'ai_score')
    dealer_score_lv = ctrl.Antecedent(np.arange(0, 32, 1), 'dealer_score')
    decision = ctrl.Consequent(np.arange(0, 2, 1), 'decision')
    
    # Membership functions for AI and dealer scores
    ai_score_lv['very_low'] = fuzz.trapmf(ai_score_lv.universe, [0, 0, 5, 10])
    ai_score_lv['low'] = fuzz.trimf(ai_score_lv.universe, [5, 10, 15])
    ai_score_lv['medium'] = fuzz.trimf(ai_score_lv.universe, [10, 15, 18])
    ai_score_lv['high'] = fuzz.trimf(ai_score_lv.universe, [15, 18, 21])
    ai_score_lv['very_high'] = fuzz.trapmf(ai_score_lv.universe, [18, 21, 32, 32])
    
    dealer_score_lv['very_low'] = fuzz.trapmf(dealer_score_lv.universe, [0, 0, 5, 10])
    dealer_score_lv['low'] = fuzz.trimf(dealer_score_lv.universe, [5, 10, 15])
    dealer_score_lv['medium'] = fuzz.trimf(dealer_score_lv.universe, [10, 15, 18])
    dealer_score_lv['high'] = fuzz.trimf(dealer_score_lv.universe, [15, 18, 21])
    dealer_score_lv['very_high'] = fuzz.trapmf(dealer_score_lv.universe, [18, 21, 32, 32])
    
    # Membership functions for decision
    decision['stand'] = fuzz.trimf(decision.universe, [0, 0, 1])
    decision['hit'] = fuzz.trimf(decision.universe, [0, 1, 1])
    
    # Fuzzy rules
    rule1 = ctrl.Rule(ai_score_lv['very_low'] | (ai_score_lv['low'] & dealer_score_lv['very_high']), decision['hit'])
    rule2 = ctrl.Rule(ai_score_lv['medium'] & dealer_score_lv['medium'], decision['hit'])
    rule3 = ctrl.Rule(ai_score_lv['high'] & dealer_score_lv['low'], decision['stand'])
    rule4 = ctrl.Rule(ai_score_lv['very_high'], decision['stand'])
    rule5 = ctrl.Rule(ai_score_lv['low'] & dealer_score_lv['high'], decision['hit'])
    rule6 = ctrl.Rule(ai_score_lv['very_low'] & dealer_score_lv['very_low'], decision['hit'])
    rule7 = ctrl.Rule(ai_score_lv['medium'] & dealer_score_lv['very_low'], decision['hit'])
    rule8 = ctrl.Rule(ai_score_lv['high'] & dealer_score_lv['very_high'], decision['stand'])
    
    ai_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
    ai_decision = ctrl.ControlSystemSimulation(ai_ctrl)
    
    # Input current scores
    ai_decision.input['ai_score'] = ai_score
    ai_decision.input['dealer_score'] = dealer_score
    ai_decision.compute()
    
    # Get the AI decision (hit or stand)
    decision_value = ai_decision.output['decision']
    
    # Ensure AI doesn't bust
    if decision_value >= 0.5:
        potential_score = calculate_score(hand + [current_deck[0]])  # Check potential score with the next card
        if potential_score <= 21:
            hand, current_deck = deal_cards(hand, current_deck)
        else:
            # Force the AI to stand if hitting would cause a bust
            decision_value = 0.0
    
    return hand, current_deck