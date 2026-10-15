from typing import Any


def _agent_map(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {agent["id"]: agent for agent in config["agents"]}


def _entry(
    turn: int,
    agent: str,
    message: str,
    offer: Any = None,
) -> dict[str, Any]:
    return {
        "turn": turn,
        "agent": agent,
        "message": message,
        "offer": offer,
    }


def _result(
    config: dict[str, Any],
    transcript: list[dict[str, Any]],
    status: str,
    agreed_price: float | None,
    turns_used: int,
    agreement_details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "scenarioId": config["scenarioId"],
        "scenarioName": config["scenarioName"],
        "status": status,
        "agreedPrice": agreed_price,
        "agreementDetails": agreement_details,
        "turnsUsed": turns_used,
        "transcript": transcript,
        "engine": "mock",
    }


def negotiate_vendor_pricing(
    config: dict[str, Any],
    max_turns: int = 6,
) -> dict[str, Any]:
    agents = _agent_map(config)
    buyer = agents.get("buyer")
    vendor = agents.get("vendor")

    if not buyer or not vendor:
        raise ValueError("Vendor Pricing requires buyer and vendor agents.")

    budget = 80000
    minimum = 65000

    buyer_personality = buyer["personality"]
    vendor_personality = vendor["personality"]

    buyer_offer = {
        "Aggressive": 65000,
        "Collaborative": 70000,
        "Risk-Averse": 66000,
    }[buyer_personality]

    vendor_offer = {
        "Aggressive": 80000,
        "Collaborative": 76000,
        "Risk-Averse": 75000,
    }[vendor_personality]

    transcript = [
        _entry(
            0,
            "Orchestrator",
            "Vendor pricing negotiation started.",
        )
    ]

    agreement = None
    turns_used = 0

    for turn in range(1, max_turns + 1):
        turns_used = turn
        buyer_offer = min(buyer_offer, budget)

        transcript.append(
            _entry(
                turn,
                buyer["name"],
                f"Buyer offers ₹{buyer_offer:,} for the licenses.",
                buyer_offer,
            )
        )

        if minimum <= buyer_offer <= budget:
            agreement = buyer_offer
            transcript.append(
                _entry(
                    turn,
                    vendor["name"],
                    f"Vendor accepts ₹{agreement:,}.",
                    agreement,
                )
            )
            break

        gap = max(0, vendor_offer - buyer_offer)
        concession = max(1000, gap // 2)
        vendor_offer = max(minimum, vendor_offer - concession)

        transcript.append(
            _entry(
                turn,
                vendor["name"],
                f"Vendor counter-offers ₹{vendor_offer:,}.",
                vendor_offer,
            )
        )

        if minimum <= vendor_offer <= budget:
            agreement = vendor_offer
            transcript.append(
                _entry(
                    turn,
                    buyer["name"],
                    f"Buyer accepts ₹{agreement:,}.",
                    agreement,
                )
            )
            break

        buyer_offer = min(
            budget,
            buyer_offer + max(1000, (vendor_offer - buyer_offer) // 2),
        )

    status = "agreement" if agreement is not None else "no_agreement"

    transcript.append(
        _entry(
            turns_used,
            "Orchestrator",
            (
                f"Final agreed price: ₹{agreement:,}."
                if agreement is not None
                else "No agreement reached within the turn limit."
            ),
            agreement,
        )
    )

    return _result(
        config,
        transcript,
        status,
        agreement,
        turns_used,
    )


def negotiate_job_offer(
    config: dict[str, Any],
    max_turns: int = 6,
) -> dict[str, Any]:
    agents = _agent_map(config)
    candidate = agents.get("candidate")
    recruiter = agents.get("recruiter")

    if not candidate or not recruiter:
        raise ValueError("Job Offer requires candidate and recruiter agents.")

    # Illustrative salary figures in LPA.
    candidate_minimum = 9.0
    candidate_target = 11.0
    recruiter_maximum = 10.0

    candidate_personality = candidate["personality"]
    recruiter_personality = recruiter["personality"]

    candidate_offer = {
        "Aggressive": 11.0,
        "Collaborative": 10.5,
        "Risk-Averse": 10.0,
    }[candidate_personality]

    recruiter_offer = {
        "Aggressive": 9.0,
        "Collaborative": 9.5,
        "Risk-Averse": 9.2,
    }[recruiter_personality]

    transcript = [_entry(0, "Orchestrator", "Job offer negotiation started.")]

    agreement = None
    turns_used = 0

    # No feasible agreement exists if candidate's minimum exceeds
    # the recruiter's maximum approved salary.
    if candidate_minimum > recruiter_maximum:
        transcript.append(
            _entry(
                1,
                "Orchestrator",
                "No overlap between candidate minimum and recruiter maximum.",
            )
        )
        return _result(
            config,
            transcript,
            "no_agreement",
            None,
            0,
        )

    for turn in range(1, max_turns + 1):
        turns_used = turn
        candidate_offer = min(candidate_offer, candidate_target)

        transcript.append(
            _entry(
                turn,
                candidate["name"],
                f"Candidate requests {candidate_offer:.1f} LPA.",
                candidate_offer,
            )
        )

        if candidate_minimum <= candidate_offer <= recruiter_maximum:
            agreement = candidate_offer
            transcript.append(
                _entry(
                    turn,
                    recruiter["name"],
                    f"Recruiter accepts {agreement:.1f} LPA.",
                    agreement,
                )
            )
            break

        recruiter_offer = min(
            recruiter_maximum,
            recruiter_offer
            + max(
                0.2,
                (candidate_offer - recruiter_offer) / 2,
            ),
        )

        transcript.append(
            _entry(
                turn,
                recruiter["name"],
                f"Recruiter counter-offers {recruiter_offer:.1f} LPA.",
                recruiter_offer,
            )
        )

        if candidate_minimum <= recruiter_offer <= recruiter_maximum:
            agreement = recruiter_offer
            transcript.append(
                _entry(
                    turn,
                    candidate["name"],
                    f"Candidate accepts {agreement:.1f} LPA.",
                    agreement,
                )
            )
            break

        candidate_offer = max(
            candidate_minimum,
            candidate_offer
            - max(
                0.2,
                (candidate_offer - recruiter_offer) / 2,
            ),
        )

    status = "agreement" if agreement is not None else "no_agreement"

    transcript.append(
        _entry(
            turns_used,
            "Orchestrator",
            (
                f"Final agreed salary: {agreement:.1f} LPA."
                if agreement is not None
                else "No salary agreement reached within the turn limit."
            ),
            agreement,
        )
    )

    return _result(
        config,
        transcript,
        status,
        agreement,
        turns_used,
        {"salaryLpa": agreement} if agreement is not None else None,
    )


def negotiate_project_budget(
    config: dict[str, Any],
    max_turns: int = 6,
) -> dict[str, Any]:
    agents = _agent_map(config)
    manager = agents.get("project-manager")

    department_agents = [
        agent for agent in config["agents"] if agent["id"] != "project-manager"
    ]

    if not manager or not department_agents:
        raise ValueError(
            "Project Budget requires a project manager and department leads."
        )

    # Illustrative example: total budget ₹10 lakh.
    total_budget = 10.0
    requested_allocations = {
        "development-lead": 5.0,
        "testing-lead": 2.0,
        "operations-lead": 3.0,
    }

    transcript = [_entry(0, "Orchestrator", "Project budget allocation started.")]

    turns_used = 1
    requested_total = 0.0
    allocations = {}

    for agent in department_agents:
        amount = requested_allocations.get(agent["id"])

        if amount is None:
            # Unknown department: use an equal-share illustrative request.
            amount = total_budget / len(department_agents)

        allocations[agent["id"]] = amount
        requested_total += amount

        transcript.append(
            _entry(
                1,
                agent["name"],
                f"Requests ₹{amount:.2f} lakh for its department.",
                amount,
            )
        )

    if requested_total <= total_budget:
        final_allocations = allocations
        status = "agreement"
        message = (
            f"Requested allocations total ₹{requested_total:.2f} lakh "
            "and fit within the project budget."
        )
    else:
        # Proportionally reduce requests if the total exceeds the budget.
        scale = total_budget / requested_total
        final_allocations = {
            agent_id: round(amount * scale, 2)
            for agent_id, amount in allocations.items()
        }

        # Correct rounding difference so allocations do not exceed budget.
        difference = round(
            total_budget - sum(final_allocations.values()),
            2,
        )
        first_id = next(iter(final_allocations))
        final_allocations[first_id] = round(
            final_allocations[first_id] + difference,
            2,
        )

        status = "agreement"
        message = (
            "The requested total exceeded the budget. "
            "The orchestrator adjusted allocations proportionally."
        )

    turns_used = 2

    transcript.append(
        _entry(
            2,
            manager["name"],
            message,
            final_allocations,
        )
    )

    for agent in department_agents:
        amount = final_allocations[agent["id"]]
        transcript.append(
            _entry(
                2,
                agent["name"],
                f"Final allocation: ₹{amount:.2f} lakh.",
                amount,
            )
        )

    total_allocated = round(sum(final_allocations.values()), 2)

    transcript.append(
        _entry(
            2,
            "Orchestrator",
            (
                f"Final allocation total: ₹{total_allocated:.2f} lakh "
                f"out of ₹{total_budget:.2f} lakh."
            ),
            total_allocated,
        )
    )

    return _result(
        config,
        transcript,
        status,
        None,
        turns_used,
        {
            "totalBudgetLakh": total_budget,
            "allocationsLakh": final_allocations,
            "totalAllocatedLakh": total_allocated,
        },
    )


def run_negotiation(
    config: dict[str, Any],
    max_turns: int = 6,
) -> dict[str, Any]:
    scenario_id = config["scenarioId"]

    if scenario_id == "vendor-pricing":
        return negotiate_vendor_pricing(config, max_turns)

    if scenario_id in ("job-offer", "job-offer-negotiation"):
        return negotiate_job_offer(config, max_turns)

    if scenario_id in (
        "project-budget",
        "project-budget-allocation",
    ):
        return negotiate_project_budget(config, max_turns)

    raise ValueError(
        f"Unsupported scenario ID: {scenario_id}. "
        "Supported scenarios: vendor-pricing, job-offer, project-budget."
    )
