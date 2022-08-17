from cashflower import assign, ModelVariable
from cashflower.utils import get_cell

from wol.assumption import assumption
from wol.modelpoint import policy


age = ModelVariable()
death_prob = ModelVariable()
survival_rate = ModelVariable()
expected_premium = ModelVariable()
expected_benefit = ModelVariable()
projection_year = ModelVariable(recalc=False)
yearly_spot_rate = ModelVariable(recalc=False)
yearly_forward_rate = ModelVariable(recalc=False)
forward_rate = ModelVariable(recalc=False)
discount_rate = ModelVariable(recalc=False)
pv_expected_premium = ModelVariable()
pv_expected_benefit = ModelVariable()
best_estimate_liabilities = ModelVariable()


@assign(age)
def age_formula(t):
    if t == 0:
        return int(policy.get("AGE"))
    elif t % 12 == 0:
        return age(t-1) + 1
    else:
        return age(t-1)


@assign(death_prob)
def death_prob_formula(t):
    sex = policy.get("SEX")
    if age(t) == age(t-1):
        return death_prob(t-1)
    elif age(t) <= 100:
        yearly_rate = float(get_cell(assumption["mortality"], sex, AGE=age(t)))
        monthly_rate = (1 - (1 - yearly_rate)**(1/12))
        return monthly_rate
    else:
        return 1


@assign(survival_rate)
def survival_rate_formula(t):
    if t == 0:
        return 1 - death_prob(t)
    else:
        return survival_rate(t-1) * (1 - death_prob(t))


@assign(expected_premium)
def expected_premium_formula(t):
    premium = float(policy.get("PREMIUM"))
    return premium * survival_rate(t-1)


@assign(expected_benefit)
def expected_benefit_formula(t):
    sum_assured = float(policy.get("SUM_ASSURED"))
    return survival_rate(t-1) * death_prob(t) * sum_assured


@assign(projection_year)
def projection_year_formula(t):
    if t == 0:
        return 0
    elif t % 12 == 1:
        return projection_year(t - 1) + 1
    else:
        return projection_year(t - 1)


@assign(yearly_spot_rate)
def yearly_spot_rate_formula(t):
    if t == 0:
        return 0
    else:
        return get_cell(assumption["interest_rates"], "VALUE", T=projection_year(t))


@assign(yearly_forward_rate)
def yearly_forward_rate_formula(t):
    if t == 0:
        return 0
    elif t == 1:
        return yearly_spot_rate(t)
    elif t % 12 != 1:
        return yearly_forward_rate(t-1)
    else:
        return ((1+yearly_spot_rate(t))**projection_year(t))/((1+yearly_spot_rate(t-1))**projection_year(t-1)) - 1


@assign(forward_rate)
def forward_rate_formula(t):
    return (1+yearly_forward_rate(t))**(1/12)-1


@assign(discount_rate)
def discount_rate_formula(t):
    return 1/(1+forward_rate(t))


@assign(pv_expected_premium)
def pv_expected_premium_formula(t):
    return expected_premium(t) + pv_expected_premium(t+1) * discount_rate(t)


@assign(pv_expected_benefit)
def pv_expected_benefit_formula(t):
    return expected_benefit(t) + pv_expected_benefit(t+1) * discount_rate(t)


@assign(best_estimate_liabilities)
def best_estimate_liabilities_formula(t):
    return pv_expected_benefit(t) - pv_expected_premium(t)
