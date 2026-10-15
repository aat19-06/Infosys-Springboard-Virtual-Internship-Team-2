
 // Scenario configuration for the Multi-Agent Negotiation Simulator.
// React can import `scenarios` and use the selected scenario's agents.
//
// IMPORTANT - ILLUSTRATIVE VALUES:
// Every INR amount, salary limit, and budget allocation in this file is an
// illustrative example value. None of them are specified by the assignment.
// They were chosen only so that each scenario has a realistic negotiation
// range, and they can be changed freely.
//
// If you change a number, update BOTH the constraint text and the matching
// `exampleValues` entry on that scenario. validateScenarios() cross-checks the
// `exampleValues` (e.g. that the example allocations do not exceed the total
// budget) so the example numbers stay consistent.

export const scenarios = [
  {
    id: "vendor-pricing",
    name: "Vendor Pricing Negotiation",
    description:
      "A buyer and a vendor negotiate the price and terms for purchasing 100 software licenses. (All figures are illustrative example values, not assignment-specified.)",
    // Example values (illustrative). The buyer's maximum (₹80,000) is above the
    // vendor's minimum (₹65,000), so an agreement is possible between them.
    exampleValues: {
      licenses: 100,
      buyerMaxBudgetINR: 80000,
      vendorMinPriceINR: 65000
    },
    agents: [
      {
        id: "buyer",
        name: "Buyer Agent",
        role: "Buyer",
        roleDescription: "Represents the purchasing company during the negotiation.",
        goal: "Purchase 100 software licenses at a reasonable total price while meeting quality requirements.",
        constraints: [
          "The total budget must not exceed ₹80,000.",
          "The software must meet the buyer's minimum quality and support requirements.",
          "The buyer must not agree to a price above the approved budget."
        ],
        defaultPersonality: "Risk-Averse"
      },
      {
        id: "vendor",
        name: "Vendor Agent",
        role: "Vendor",
        roleDescription: "Represents the software seller and negotiates the commercial terms.",
        goal: "Close the sale at a profitable price while maintaining the expected service quality.",
        constraints: [
          "The total selling price must be at least ₹65,000.",
          "The vendor must not promise services that are not included in the offer.",
          "The vendor must maintain the agreed software quality and support."
        ],
        defaultPersonality: "Aggressive"
      }
    ]
  },
  {
    id: "job-offer",
    name: "Job Offer Negotiation",
    description:
      "A job candidate and a recruiter negotiate salary, benefits, and employment terms. (All figures are illustrative example values, not assignment-specified.)",
    // Example values (illustrative), in LPA (lakhs per annum).
    // - candidateTargetLPA: the candidate's ideal outcome.
    // - candidateMinimumLPA: the lowest salary the candidate will accept.
    // - recruiterMaxLPA: the recruiter's approved maximum offer.
    // The agreement zone is ₹9-10 LPA.
    exampleValues: {
      candidateTargetLPA: 11,
      candidateMinimumLPA: 9,
      recruiterMaxLPA: 10
    },
    agents: [
      {
        id: "candidate",
        name: "Candidate Agent",
        role: "Job Candidate",
        roleDescription: "Represents the applicant negotiating an employment offer.",
        goal: "Obtain a competitive salary and suitable benefits for the role.",
        constraints: [
          "The target salary is ₹11 LPA (the candidate's ideal outcome).",
          "The minimum acceptable salary is ₹9 LPA; the candidate must not accept a base salary below this.",
          "The candidate must consider the responsibilities and benefits, not salary alone.",
          "The candidate must not claim qualifications or experience they do not have."
        ],
        defaultPersonality: "Collaborative"
      },
      {
        id: "recruiter",
        name: "Recruiter Agent",
        role: "Employer Representative",
        roleDescription: "Represents the hiring company and manages the employment offer.",
        goal: "Hire a suitable candidate on terms that fit the company's compensation budget.",
        constraints: [
          "The salary offer must not exceed the approved maximum of ₹10 LPA.",
          "The offer must meet the role's approved requirements and policies.",
          "The recruiter must not promise unapproved benefits."
        ],
        defaultPersonality: "Risk-Averse"
      }
    ]
  },
  {
    id: "project-budget",
    name: "Project Budget Allocation",
    description:
      "A project manager and department leads negotiate how to allocate a limited project budget. (All figures are illustrative example values, not assignment-specified.)",
    // Example values in lakhs: 5 + 2 + 3 = ₹10 lakh.
    // This leaves no unallocated reserve.
    exampleValues: {
      totalLakh: 10,
      requestsLakh: {
        "development-lead": 5,
        "testing-lead": 2,
        "operations-lead": 3
      }
    },
    agents: [
      {
        id: "project-manager",
        name: "Project Manager Agent",
        role: "Project Manager",
        roleDescription: "Coordinates the project and balances the needs of all departments.",
        goal: "Allocate the available budget so essential project work can be completed.",
        constraints: [
          "The total project budget is ₹10 lakh.",
          "The final allocations must not exceed the total budget.",
          "Essential project activities must receive sufficient funding."
        ],
        defaultPersonality: "Risk-Averse"
      },
      {
        id: "development-lead",
        name: "Development Lead Agent",
        role: "Development Department Representative",
        roleDescription: "Represents the team responsible for building the project.",
        goal: "Secure sufficient funding for development work and required technical resources.",
        constraints: [
          "The requested allocation is ₹5 lakh.",
          "The department must explain the need for requested funds.",
          "The allocation must fit within the overall project budget."
        ],
        defaultPersonality: "Aggressive"
      },
      {
        id: "testing-lead",
        name: "Testing Lead Agent",
        role: "Testing Department Representative",
        roleDescription: "Represents the team responsible for testing and quality assurance.",
        goal: "Secure enough funding to test the project and reduce defects.",
        constraints: [
          "The requested allocation is ₹2 lakh.",
          "The department must prioritize essential testing activities.",
          "The allocation must fit within the overall project budget."
        ],
        defaultPersonality: "Collaborative"
      },
      {
        id: "operations-lead",
        name: "Operations Lead Agent",
        role: "Operations Department Representative",
        roleDescription: "Represents the team responsible for deployment and ongoing operations.",
        goal: "Secure enough funding for deployment, monitoring, and maintenance.",
        constraints: [
          "The requested allocation is ₹3 lakh.",
          "The department must prioritize essential operational needs.",
          "The allocation must fit within the overall project budget."
        ],
        defaultPersonality: "Collaborative"
      }
    ]
  }
];

export const PERSONALITIES = ["Aggressive", "Collaborative", "Risk-Averse"];

const isNonEmptyString = (value) =>
  typeof value === "string" && value.trim().length > 0;

const isPositiveNumber = (value) =>
  typeof value === "number" && Number.isFinite(value) && value > 0;

// Cross-check a scenario's illustrative example values.
function validateExampleValues(scenario, label, errors) {
  const values = scenario.exampleValues;
  if (values === undefined) return;

  if (values === null || typeof values !== "object" || Array.isArray(values)) {
    errors.push(`${label}: exampleValues must be an object.`);
    return;
  }

  switch (scenario.id) {
    case "vendor-pricing": {
      const { buyerMaxBudgetINR, vendorMinPriceINR } = values;
      if (!isPositiveNumber(buyerMaxBudgetINR) || !isPositiveNumber(vendorMinPriceINR)) {
        errors.push(
          `${label}: buyer budget and vendor minimum price must be positive numbers.`
        );
      } else if (vendorMinPriceINR > buyerMaxBudgetINR) {
        errors.push(
          `${label}: vendor minimum price (${vendorMinPriceINR}) is above the buyer's maximum budget (${buyerMaxBudgetINR}), so no agreement is possible.`
        );
      }
      break;
    }

    case "job-offer": {
      const { candidateTargetLPA, candidateMinimumLPA, recruiterMaxLPA } = values;

      if (
        !isPositiveNumber(candidateTargetLPA) ||
        !isPositiveNumber(candidateMinimumLPA) ||
        !isPositiveNumber(recruiterMaxLPA)
      ) {
        errors.push(
          `${label}: candidate salary values must all be positive numbers.`
        );
        break;
      }

      if (candidateMinimumLPA > candidateTargetLPA) {
        errors.push(
          `${label}: candidate minimum acceptable salary is above their target salary.`
        );
      }

      if (candidateMinimumLPA > recruiterMaxLPA) {
        errors.push(
          `${label}: candidate minimum salary is above the recruiter's maximum, so no agreement is possible.`
        );
      }
      break;
    }

    case "project-budget": {
      const { totalLakh, requestsLakh } = values;

      if (!isPositiveNumber(totalLakh)) {
        errors.push(`${label}: totalLakh must be a positive number.`);
        break;
      }

      if (!requestsLakh || typeof requestsLakh !== "object" || Array.isArray(requestsLakh)) {
        errors.push(`${label}: requestsLakh must be an object keyed by agent id.`);
        break;
      }

      const agentIds = new Set((scenario.agents || []).map((agent) => agent?.id));
      let allocated = 0;

      for (const [agentId, amount] of Object.entries(requestsLakh)) {
        if (!agentIds.has(agentId)) {
          errors.push(`${label}: unknown allocation agent "${agentId}".`);
        }

        if (!isPositiveNumber(amount)) {
          errors.push(`${label}: allocation for "${agentId}" must be positive.`);
        } else {
          allocated += amount;
        }
      }

      if (allocated > totalLakh + 1e-9) {
        errors.push(
          `${label}: example allocations total ₹${allocated} lakh, exceeding the total budget of ₹${totalLakh} lakh.`
        );
      }
      break;
    }

    default:
      break;
  }
}

// Validate scenario data before it is used by the application.
export function validateScenarios(items = scenarios) {
  const errors = [];
  const validPersonalities = new Set(PERSONALITIES);
  const requiredScenarioIds = ["vendor-pricing", "job-offer", "project-budget"];

  if (!Array.isArray(items)) {
    return { valid: false, errors: ["Scenarios must be an array."] };
  }

  for (const id of requiredScenarioIds) {
    if (!items.some((scenario) => scenario?.id === id)) {
      errors.push(`Missing required scenario: ${id}`);
    }
  }

  const seenScenarioIds = new Set();

  for (const [scenarioIndex, scenario] of items.entries()) {
    const label = scenario?.name || `Scenario at index ${scenarioIndex}`;

    if (!isNonEmptyString(scenario?.id)) {
      errors.push(`${label}: missing id.`);
    } else if (seenScenarioIds.has(scenario.id)) {
      errors.push(`${label}: duplicate scenario id "${scenario.id}".`);
    } else {
      seenScenarioIds.add(scenario.id);
    }

    if (!isNonEmptyString(scenario?.name)) errors.push(`${label}: missing name.`);
    if (!isNonEmptyString(scenario?.description)) errors.push(`${label}: missing description.`);

    if (!Array.isArray(scenario?.agents) || scenario.agents.length === 0) {
      errors.push(`${label}: agents must be a non-empty array.`);
      continue;
    }

    const seenAgentIds = new Set();

    for (const [agentIndex, agent] of scenario.agents.entries()) {
      const agentLabel = agent?.name || `Agent at index ${agentIndex} in ${label}`;

      if (!isNonEmptyString(agent?.id)) {
        errors.push(`${agentLabel}: missing id.`);
      } else if (seenAgentIds.has(agent.id)) {
        errors.push(`${agentLabel}: duplicate agent id "${agent.id}" in ${label}.`);
      } else {
        seenAgentIds.add(agent.id);
      }

      if (!isNonEmptyString(agent?.name)) errors.push(`${agentLabel}: missing name.`);
      if (!isNonEmptyString(agent?.role)) errors.push(`${agentLabel}: missing role.`);
      if (!isNonEmptyString(agent?.roleDescription)) {
        errors.push(`${agentLabel}: missing roleDescription.`);
      }
      if (!isNonEmptyString(agent?.goal)) errors.push(`${agentLabel}: missing goal.`);

      if (!Array.isArray(agent?.constraints) || agent.constraints.length === 0) {
        errors.push(`${agentLabel}: constraints must be a non-empty array.`);
      } else if (!agent.constraints.every(isNonEmptyString)) {
        errors.push(`${agentLabel}: constraints must contain only non-empty strings.`);
      }

      if (!validPersonalities.has(agent?.defaultPersonality)) {
        errors.push(`${agentLabel}: invalid defaultPersonality.`);
      }
    }

    validateExampleValues(scenario, label, errors);
  }

  return { valid: errors.length === 0, errors };
}
