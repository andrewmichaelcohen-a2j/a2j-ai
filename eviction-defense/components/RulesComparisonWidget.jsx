import { useState } from "react";

// ─── DATA ────────────────────────────────────────────────────────────────────

const JURISDICTIONS = ["CA", "TX", "NY"];

const FACT_PATTERNS = {
  CA: {
    state: "California", city: "Los Angeles",
    noticeType: "3-Day Pay or Quit",
    amount: "$1,850 rent + $200 late fees ($2,050 total)",
    tenancy: "3 years", servedBy: "Post and mail (nail and mail)",
  },
  TX: {
    state: "Texas", city: "Houston",
    noticeType: "3-Day Notice to Vacate",
    amount: "$1,850 rent + $200 late fees ($2,050 total)",
    tenancy: "3 years", servedBy: "Posted on door",
  },
  NY: {
    state: "New York", city: "New York City",
    noticeType: "3-Day Rent Demand",
    amount: "$1,850 rent + $200 late fees ($2,050 total)",
    tenancy: "3 years", servedBy: "Personal delivery",
  },
};

const LLM_RESPONSES = {
  CA: {
    text: `Based on California law, a 3-Day Pay or Quit notice requires the tenant to pay the full amount owed or vacate within 3 days. The notice appears to be valid.

The total amount demanded ($2,050) includes both unpaid rent and late fees, which is standard practice for California notices.

The notice was served by nail-and-mail, which is a recognized service method in California.

Recommendation: You must pay $2,050 or vacate within 3 days of the notice date.`,
    defectsFound: 0,
    sourceCited: false,
    statusBadge: "Based on training data (knowledge cutoff: 2024)",
    statusType: "warning",
  },
  TX: {
    text: `Under Texas law, a 3-Day Notice to Vacate is the standard notice for nonpayment of rent. The notice period appears correct.

Texas does not have statewide rent control or just-cause eviction requirements, so the landlord may terminate the tenancy with proper notice.

The amount demanded ($2,050) reflects rent and fees owed. The notice appears valid.

Recommendation: Pay the full amount or vacate within 3 days.`,
    defectsFound: 0,
    sourceCited: false,
    statusBadge: "Based on training data (knowledge cutoff: 2024)",
    statusType: "warning",
  },
  NY: {
    text: `Under New York law, landlords can serve a 3-Day Rent Demand for nonpayment of rent. The tenant must pay or vacate within 3 days.

The notice appears to be properly served by personal delivery.

The total amount of $2,050 includes rent and fees owed under the lease.

Recommendation: Pay the demanded amount or vacate within 3 days to avoid eviction proceedings.`,
    defectsFound: 0,
    sourceCited: false,
    statusBadge: "Based on training data (knowledge cutoff: 2024)",
    statusType: "warning",
  },
};

const RULES_RESPONSES = {
  CA: {
    rulesFile: "ca_eviction_v1.2.json (DRAFT)",
    defects: [
      {
        id: "CA-DEFECT-01",
        title: "Late fees included in notice amount",
        detail: "California law (CCP §1161(2)) prohibits including late fees in a Pay or Quit notice. Only unpaid rent may be demanded. The $200 late fee renders this notice void.",
        statute: "CCP §1161(2)",
        severity: "INVALID",
      },
      {
        id: "CA-DEFECT-02",
        title: "Incorrect notice period for tenancy length",
        detail: "For a tenancy of 3 years, California requires a 15-day Pay or Quit notice (not 3 days) under AB 1482. CCP §1161(2), as amended by AB 1482.",
        statute: "CCP §1161(2); AB 1482",
        severity: "INVALID",
        validationNote: "15-day period requires attorney confirmation",
      },
    ],
    defenses: ["Habitability (uninhabitable conditions)", "Retaliatory eviction", "LA RSO just-cause requirement (LAMC 151.09)"],
    localOverlay: "Los Angeles RSO applies to pre-1978 multi-unit buildings — additional just-cause protections may apply.",
    nextStep: "Contact a legal aid attorney immediately. This notice may be void.",
    statusBadge: "Grounded in LHC rules file ca_eviction_v1.2.json",
  },
  TX: {
    rulesFile: "tx_eviction_v0.1.json (DRAFT)",
    defects: [
      {
        id: "TX-DEFECT-01",
        title: "CARES Act check required",
        detail: "If this property has a federally backed mortgage or receives HUD/Section 8 assistance, a 30-day notice is required under the CARES Act (§4024), not 3 days. Verify property status.",
        statute: "CARES Act §4024",
        severity: "POTENTIALLY_INVALID",
      },
    ],
    defenses: ["Habitability", "Retaliatory eviction", "Discrimination"],
    localOverlay: "Texas has no statewide just-cause requirement. No statewide rent control. Check CARES Act applicability.",
    nextStep: "Verify whether property has federally backed mortgage. Contact Texas legal aid immediately.",
    statusBadge: "Grounded in LHC rules file tx_eviction_v0.1.json",
    comparisonNote: "Notice: Texas analysis is shorter — simpler law, fewer notice types. Same reasoning engine, different rules file.",
  },
  NY: {
    rulesFile: "ny_eviction_rules_v0.1.json (DRAFT)",
    defects: [
      {
        id: "NY-DEFECT-01",
        title: "Incorrect notice period — NY requires 14 days",
        detail: "New York law (RPAPL §711(2), as amended by the Housing Stability and Tenant Protection Act of 2019) requires a 14-day notice for nonpayment — not 3 days. A 3-day notice in New York is legally defective.",
        statute: "RPAPL §711(2); HSTPA 2019",
        severity: "INVALID",
      },
    ],
    defenses: ["Habitability (RPL §235-b)", "Retaliatory eviction (RPL §223-b)", "NYC rent stabilization (if applicable)", "Good Cause Eviction Law (2024)"],
    localOverlay: "If unit is in NYC: check rent stabilization status. Good Cause Eviction Law (2024) may require stated reason for termination.",
    nextStep: "This notice is defective in New York. Contact NYC legal aid immediately — do not vacate.",
    statusBadge: "Grounded in LHC rules file ny_eviction_rules_v0.1.json",
  },
};

const RULES_SNIPPETS = {
  CA: `"notice_defects": [
  {
    "defect": "includes_late_fees",
    "result": "INVALID",
    "statute": "CCP §1161(2)",
    "note": "Any amount other than unpaid
             rent renders notice void"
  },
  {
    "defect": "incorrect_period_over_1yr",
    "result": "INVALID",
    "note": "15-day minimum for tenancies
             12+ months (AB 1482)"
  }
]`,
  TX: `"notice_defects": [
  {
    "defect": "cares_act_noncompliance",
    "result": "POTENTIALLY_INVALID",
    "note": "30-day notice required for
             federally backed properties"
  }
],
"just_cause_required": false,
"statewide_rent_control": false`,
  NY: `"notice_defects": [
  {
    "defect": "insufficient_notice_period",
    "result": "INVALID",
    "statute": "RPAPL §711(2)",
    "note": "NY requires 14-day notice
             (HSTPA 2019), not 3 days"
  }
]`,
};

// ─── COMPONENT ────────────────────────────────────────────────────────────────

export default function RulesComparisonWidget() {
  const [jurisdiction, setJurisdiction] = useState("CA");
  const [showWhy, setShowWhy] = useState(false);
  const [showSnippet, setShowSnippet] = useState(false);

  const facts = FACT_PATTERNS[jurisdiction];
  const llm = LLM_RESPONSES[jurisdiction];
  const rules = RULES_RESPONSES[jurisdiction];
  const snippet = RULES_SNIPPETS[jurisdiction];

  const severityColor = (s) =>
    s === "INVALID" ? "#dc2626" : s === "POTENTIALLY_INVALID" ? "#d97706" : "#16a34a";

  return (
    <div style={{ fontFamily: "'Calibri', 'Segoe UI', sans-serif", maxWidth: 1100, margin: "0 auto", padding: "16px" }}>

      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 20 }}>
        <h2 style={{ fontSize: 22, fontWeight: "bold", color: "#0D2137", margin: "0 0 6px" }}>
          Rules File vs. Raw AI: The Difference That Matters
        </h2>
        <p style={{ fontSize: 13, color: "#4A5568", margin: 0 }}>
          Same tenant. Same notice. Two very different answers.
        </p>
      </div>

      {/* Jurisdiction switcher */}
      <div style={{ display: "flex", justifyContent: "center", gap: 10, marginBottom: 18 }}>
        <span style={{ fontSize: 13, color: "#4A5568", alignSelf: "center" }}>Jurisdiction:</span>
        {JURISDICTIONS.map((j) => (
          <button
            key={j}
            onClick={() => setJurisdiction(j)}
            style={{
              padding: "6px 18px", borderRadius: 6, border: "2px solid",
              borderColor: jurisdiction === j ? "#1B5E8C" : "#CBD5E0",
              background: jurisdiction === j ? "#1B5E8C" : "#fff",
              color: jurisdiction === j ? "#fff" : "#4A5568",
              fontWeight: jurisdiction === j ? "bold" : "normal",
              fontSize: 14, cursor: "pointer",
            }}
          >
            {j}
          </button>
        ))}
      </div>

      {/* Fact pattern summary */}
      <div style={{ background: "#F0F4F8", border: "1px solid #CBD5E0", borderRadius: 8, padding: "12px 16px", marginBottom: 16, fontSize: 12.5, color: "#4A5568" }}>
        <strong style={{ color: "#1A1A2E", marginRight: 6 }}>Fact Pattern:</strong>
        Maria Garcia · {facts.city}, {facts.state} · {facts.noticeType} · {facts.amount} · Tenancy: {facts.tenancy} · Served by: {facts.servedBy}
      </div>

      {/* Two panels */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>

        {/* LEFT: Raw LLM */}
        <div style={{ border: "2px solid #FCA5A5", borderRadius: 10, overflow: "hidden" }}>
          <div style={{ background: "#FEF2F2", borderBottom: "2px solid #FCA5A5", padding: "10px 14px", display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontSize: 16 }}>⚠</span>
            <div>
              <div style={{ fontWeight: "bold", fontSize: 14, color: "#991B1B" }}>Without Rules File</div>
              <div style={{ fontSize: 11, color: "#B91C1C" }}>Raw AI response from training data</div>
            </div>
            <div style={{ marginLeft: "auto", background: "#FEE2E2", border: "1px solid #FCA5A5", borderRadius: 12, padding: "2px 10px", fontSize: 10, color: "#991B1B", fontWeight: "bold" }}>
              DEFECTS FOUND: {llm.defectsFound}
            </div>
          </div>

          <div style={{ padding: 16 }}>
            <div style={{ background: "#fff7f7", border: "1px solid #FED7D7", borderRadius: 6, padding: 14, fontSize: 12.5, color: "#1A1A2E", lineHeight: 1.7, whiteSpace: "pre-line", minHeight: 180 }}>
              {llm.text}
            </div>

            <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 6 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11.5, color: "#B91C1C" }}>
                <span>✗</span> Sources cited: None
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11.5, color: "#B91C1C" }}>
                <span>✗</span> Rules file: Not used
              </div>
              <div style={{ background: "#FEE2E2", border: "1px solid #FCA5A5", borderRadius: 6, padding: "6px 10px", fontSize: 11, color: "#991B1B", marginTop: 4 }}>
                ⚠ {llm.statusBadge}
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT: Rules-grounded */}
        <div style={{ border: "2px solid #86EFAC", borderRadius: 10, overflow: "hidden" }}>
          <div style={{ background: "#F0FDF4", borderBottom: "2px solid #86EFAC", padding: "10px 14px", display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontSize: 16 }}>✓</span>
            <div>
              <div style={{ fontWeight: "bold", fontSize: 14, color: "#14532D" }}>With LHC Rules File</div>
              <div style={{ fontSize: 11, color: "#15803D" }}>Deterministic · Cited · Auditable</div>
            </div>
            <div style={{ marginLeft: "auto", background: "#DCFCE7", border: "1px solid #86EFAC", borderRadius: 12, padding: "2px 10px", fontSize: 10, color: "#14532D", fontWeight: "bold" }}>
              DEFECTS FOUND: {rules.defects.length}
            </div>
          </div>

          <div style={{ padding: 16 }}>
            <div style={{ fontSize: 11, fontWeight: "bold", color: "#4A5568", marginBottom: 8, letterSpacing: 0.5 }}>
              NOTICE ANALYSIS — {facts.state} Eviction Notice Validator
            </div>

            {/* Defects */}
            {rules.defects.map((d) => (
              <div key={d.id} style={{ background: "#FFF7ED", border: `1px solid ${severityColor(d.severity)}`, borderLeft: `4px solid ${severityColor(d.severity)}`, borderRadius: 6, padding: "10px 12px", marginBottom: 10 }}>
                <div style={{ display: "flex", gap: 8, alignItems: "flex-start" }}>
                  <span style={{ background: severityColor(d.severity), color: "#fff", borderRadius: 4, padding: "1px 7px", fontSize: 10, fontWeight: "bold", whiteSpace: "nowrap", marginTop: 1 }}>
                    {d.severity}
                  </span>
                  <div>
                    <div style={{ fontWeight: "bold", fontSize: 12.5, color: "#1A1A2E", marginBottom: 3 }}>{d.title}</div>
                    <div style={{ fontSize: 12, color: "#4A5568", lineHeight: 1.5 }}>{d.detail}</div>
                    <div style={{ fontSize: 11, color: "#6B7280", marginTop: 4 }}>
                      Statute: <span style={{ color: "#1B5E8C", fontWeight: "bold" }}>{d.statute}</span>
                      {d.validationNote && <span style={{ color: "#D97706", marginLeft: 8 }}>⚠ {d.validationNote}</span>}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Defenses */}
            <div style={{ marginTop: 8 }}>
              <div style={{ fontSize: 11, fontWeight: "bold", color: "#4A5568", marginBottom: 5, letterSpacing: 0.5 }}>DEFENSES TO INVESTIGATE:</div>
              {rules.defenses.map((d, i) => (
                <div key={i} style={{ fontSize: 12, color: "#4A5568", marginBottom: 3 }}>• {d}</div>
              ))}
            </div>

            {/* Local overlay */}
            {rules.localOverlay && (
              <div style={{ background: "#EFF6FF", border: "1px solid #BFDBFE", borderRadius: 6, padding: "8px 12px", marginTop: 10, fontSize: 12, color: "#1e40af" }}>
                <strong>Local overlay:</strong> {rules.localOverlay}
              </div>
            )}

            {/* TX comparison note */}
            {rules.comparisonNote && (
              <div style={{ background: "#F0FDF4", border: "1px solid #86EFAC", borderRadius: 6, padding: "8px 12px", marginTop: 10, fontSize: 11.5, color: "#14532D", fontStyle: "italic" }}>
                {rules.comparisonNote}
              </div>
            )}

            {/* Next step */}
            <div style={{ background: "#0D2137", color: "#fff", borderRadius: 6, padding: "10px 14px", marginTop: 12, fontSize: 12.5, fontWeight: "bold" }}>
              Next step: {rules.nextStep}
            </div>

            {/* Status badge */}
            <div style={{ display: "flex", flexDirection: "column", gap: 5, marginTop: 10 }}>
              <div style={{ fontSize: 11.5, color: "#15803D" }}>✓ {rules.statusBadge}</div>
              <div style={{ fontSize: 11.5, color: "#15803D" }}>✓ Sources: CCP §1161(2), AB 1482, LAMC 151.09</div>
              <div style={{ fontSize: 10.5, color: "#6B7280", fontStyle: "italic" }}>
                ⚠ This is legal information, not legal advice. Verify with a licensed attorney.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Why the difference toggle */}
      <div style={{ marginTop: 16, border: "1px solid #CBD5E0", borderRadius: 8, overflow: "hidden" }}>
        <button
          onClick={() => setShowWhy(!showWhy)}
          style={{ width: "100%", background: "#F7F9FC", border: "none", padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer", fontSize: 13, fontWeight: "bold", color: "#1B5E8C" }}
        >
          <span>Why the difference?</span>
          <span>{showWhy ? "▲" : "▼"}</span>
        </button>
        {showWhy && (
          <div style={{ padding: "14px 18px", background: "#fff", fontSize: 13, color: "#4A5568", lineHeight: 1.7, borderTop: "1px solid #E2E8F0" }}>
            <p style={{ margin: "0 0 10px" }}>
              <strong style={{ color: "#1A1A2E" }}>The left panel is not broken — it's a capable AI doing its best with what it has.</strong> The problem is that it's answering from training data that may be months or years old, with no way to verify whether the law changed or to cite a specific source. It cannot know about AB 1482's notice period extension. It cannot check whether late fees are prohibited. It produces a confident-sounding answer that is wrong — and that error has real consequences for a real person.
            </p>
            <p style={{ margin: 0 }}>
              <strong style={{ color: "#1A1A2E" }}>The right panel uses the same underlying AI model.</strong> The difference is the rules file: a 45-line structured data file that encodes California eviction notice law as explicit if/then logic. The AI reads the rules file and applies it deterministically — no guessing, no inference, no hallucination. The result is auditable (you can see exactly which rule fired), citable (linked to the actual statute), and updateable (change the law → update the file → every deployment reflects the change). <strong>That is the LHC's first major community project: building and validating this library across 50 states.</strong>
            </p>
          </div>
        )}
      </div>

      {/* Rules snippet toggle */}
      <div style={{ marginTop: 10, border: "1px solid #CBD5E0", borderRadius: 8, overflow: "hidden" }}>
        <button
          onClick={() => setShowSnippet(!showSnippet)}
          style={{ width: "100%", background: "#F7F9FC", border: "none", padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer", fontSize: 13, fontWeight: "bold", color: "#0E7C87" }}
        >
          <span>See the rules file that powered this ({jurisdiction === "CA" ? "ca_eviction_v1.2.json" : jurisdiction === "TX" ? "tx_eviction_v0.1.json" : "ny_eviction_rules_v0.1.json"}) — notice_defects section</span>
          <span>{showSnippet ? "▲" : "▼"}</span>
        </button>
        {showSnippet && (
          <div style={{ borderTop: "1px solid #E2E8F0" }}>
            <div style={{ background: "#0A1520", padding: "14px 18px", fontFamily: "'Consolas', 'Monaco', monospace", fontSize: 12, color: "#B8CDD8", lineHeight: 1.8, whiteSpace: "pre" }}>
              <span style={{ color: "#7EC8A0" }}>{snippet}</span>
            </div>
            <div style={{ background: "#F0F4F8", padding: "8px 16px", fontSize: 11, color: "#6B7280", borderTop: "1px solid #E2E8F0" }}>
              DRAFT — AI-generated, not attorney-validated. Full file: github.com/andrewmichaelcohen-a2j → eviction-defense/jurisdictions/
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", marginTop: 18, fontSize: 11, color: "#9AA5B4" }}>
        Legal Help Commons · Eviction Defense Demo · v0.1 · DRAFT ·
        This is legal information, not legal advice. Not for production use with real clients.
      </div>
    </div>
  );
}
