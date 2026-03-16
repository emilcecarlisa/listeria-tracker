# GCP FY2024 Analysis: George's Foods Incident Report

**Document Date**: February 27, 2026
**Analysis of**: Poultry Good Commercial Practices (GCP) Inspection Data - FY2024 Archive

## Data Source

**File**: `data/gcpArchiveFy2024.xlsx`
**Dataset Name**: Livestock Humane Handling and Poultry Good Commercial Practices Inspection Task Dataset - Archive FY2024
**Coverage Period**: October 1, 2023 - September 30, 2024 (Fiscal Year 2024)
**Data Extracted**: March 31, 2025
**Source Authority**: USDA FSIS (Food Safety and Inspection Service)

**Data Documentation**: Available at https://www.fsis.usda.gov/sites/default/files/...
*(Reference included in dataset header)*

---

## Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Inspection Records** | 105,814 |
| **Formal Violations (NRs)** | 5 (0.005%) |
| **Memorandums of Interview (MOIs)** | 174 |
| **Clean Inspections** | 105,809 (99.995%) |
| **Time Period** | FY2024 (Oct 1, 2023 - Sep 30, 2024) |

### Key Data Elements

The dataset includes the following fields for each inspection:
- Establishment ID, Number, and Name
- Inspection Date and Type
- Task Code and Name
- Regulations Verified
- Noncompliance Records (NR) details
- Memorandum of Interview (MOI) details

---

## Understanding NRs vs MOIs: FSIS Documentation Framework

**Source**: FSIS Directive 6110.1 - "Writing Noncompliance Records and Memoranda of Interview for Good Commercial Practices and Poultry Mistreatment"

The USDA FSIS uses two distinct documentation mechanisms for poultry handling issues, each with specific criteria:

### Noncompliance Records (NRs) - Formal Violations

**When Used**: NRs are issued ONLY when Inspection Program Personnel (IPP) can demonstrate an establishment has **lost process control** with an **ongoing pattern or trend** of problems.

**Criteria for Writing an NR**:
- Repeated occurrence of birds dying otherwise than by slaughter
- Birds frequently entering the scalder while still breathing
- Birds not being appropriately bled out (e.g., equipment malfunction resulting in increased cadavers)
- Intentional and repeated mistreatment by establishment personnel
- Systemic handling practices resulting in adulterated product

**Key Questions IPP Consider**:
1. What is the problem?
2. Is equipment (bleeding/stunning) not functioning properly?
3. When did the problem occur and how long did it last?
4. How did the establishment react and correct the problem?
5. Were there periods of control?
6. Did the problem reoccur?

**Regulation Cited**: 9 CFR 381.65(b) - Failure to handle birds in accordance with Good Commercial Practices

**Important**: An **isolated instance does NOT represent a loss of process control** and should be documented in a mistreatment MOI, not an NR.

### Memorandums of Interview (MOIs) - Documented Concerns

**When Used**: MOIs are issued when IPP observe poultry mistreatment but **CANNOT support a loss of process control** by the establishment.

**Criteria for Writing an MOI**:
- **Isolated incidents** of mistreatment (not ongoing/systematic)
- Single or small numbers of birds involved
- Incident does not represent an ongoing problem
- Unusually high number of injuries (broken legs/wings) but no evidence of intentional mistreatment
- One bird enters scalder while breathing (isolated, not repeated)

**MOI Process**:
1. IPP notify the establishment immediately after observing mistreatment
2. IPP discuss the event with establishment management as soon as possible
3. MOI documents the **meeting and discussion** between IPP and establishment
4. MOI includes:
   - Date, time, and location of the event
   - Names of all participants in the meeting
   - Description of what was observed
   - Establishment's planned corrective actions
   - Any immediate responses by the establishment

**Establishment Rights**:
- Establishments may **object to MOI content** (verbally or in writing)
- Objections are documented in or attached to the MOI
- Establishments with PHIS accounts can respond electronically
- MOIs are **not formal regulatory violations**

### Why the Distinction Matters

| Aspect | Noncompliance Record (NR) | Memorandum of Interview (MOI) |
|--------|---------------------------|--------------------------------|
| **Nature** | Formal regulatory violation | Documented concern/warning |
| **Threshold** | Systemic/repeated problem | Isolated incident |
| **Process Control** | Lost control demonstrated | Control maintained |
| **Regulatory Action** | Cites 9 CFR 381.65(b) | Non-regulatory concern |
| **Product Impact** | Adulterated product produced | Potential for future issues |
| **Establishment Response** | Must correct violation | Voluntary corrective action |
| **Appeal Rights** | Can appeal per 9 CFR 306.5 | Can object to content |

**Federal Register Reference**: "Treatment of Live Poultry Before Slaughter," 70 Fed. Reg. 56624 (September 28, 2005) provides additional industry guidelines.

**DVMS Oversight**: District Veterinary Medical Specialists (DVMS) review both NRs and MOIs to ensure accuracy and consistency in documentation. In serious cases, the DVMS may collaborate with the inspection team to prepare a Letter of Concern (LOC) to establishment management and state officials.

---

## Violation Statistics

### Noncompliance Records (NRs)
Only **5 formal violations** were recorded across 105,814 inspections (0.005% violation rate).

**Top Violated Regulation**:
- **381.65(b)**: 5 violations (100% of all NRs)

**Analysis**: The extremely low NR rate (0.005%) reflects FSIS's high threshold for formal violations - requiring demonstrated loss of process control, not isolated incidents.

### Memorandums of Interview (MOIs)
**174 MOIs** were issued during FY2024 - representing a rate of 0.16% of inspections.

**What This Means**:
- MOIs are **35 times more common** than formal NRs (174 vs 5)
- Most poultry handling concerns are addressed through documented discussions rather than formal violations
- The MOI system allows IPP to address isolated incidents proactively before they become systemic problems
- Establishments can respond to concerns without formal regulatory action

---

## George's Foods Incident - April 12, 2024

### Incident Summary

**✓ CONFIRMED**: The incident was successfully located in the FY2024 archive dataset.

### Establishment Details
- **Name**: George's Foods, LLC
- **Establishment Number**: P2186
- **Establishment ID**: 2279
- **Location**: [Address redacted in dataset]

### Inspection Details
- **Date**: April 12, 2024
- **Time**: 21:05 (9:05 PM)
- **Inspection Type**: Directed
- **Task Code**: 04C05
- **Task Name**: Poultry Good Commercial Practices
- **Task ID**: {A8DC6D40-36F9-EE11-9F01-0003FF2057A2}

### Incident Documentation
- **MOI Number**: YJO3820044712G
- **MOI Date**: April 12, 2024
- **Inspector**: SPHV Dr. [REDACTED]
- **Supervisor Notified**: [REDACTED] (notified at 21:30)

### Full Incident Description

> *"At approximately 21:05 on 4/12/2024 while performing a routine Poultry Good Commercial Practices task, I, SPHV Dr. REDACTED, observed a live hang employee forcefully throw a live chicken against the wall behind him. After being thrown against the wall, the chicken lay in sternal recumbency on the floor behind the live hang belt with a rapid respiration rate, appearing to be in respiratory distress. This is an instance of mistreatment of live poultry. I informed live hang supervisor REDACTED of my findings at approximately 21:30. Poultry must be treated in a manner consistent with good commercial practices."*

### Incident Classification
- **Violation Type**: Mistreatment of live poultry
- **Regulatory Context**: Good commercial practices for poultry handling
- **Animal Welfare Concern**: Physical trauma causing respiratory distress

### Regulatory Outcome
- **Noncompliance Record (NR) Issued**: ❌ No
- **Memorandum of Interview (MOI) Issued**: ✅ Yes (YJO3820044712G)

### Why MOI Instead of NR?

Based on FSIS Directive 6110.1 criteria, this incident was documented as an MOI rather than a formal NR because:

**Evidence of Isolated Incident**:
- **Single observation**: One employee, one chicken, one incident at 21:05
- **No pattern or trend**: No evidence of repeated or systematic mistreatment
- **No loss of process control**: The establishment's GCP processes remained in control
- **Immediate notification**: Supervisor was notified within 25 minutes (at 21:30)

**NR Threshold Not Met**:
An NR would require demonstration of:
- ❌ Repeated occurrence of birds being mistreated
- ❌ Ongoing pattern of birds dying otherwise than by slaughter
- ❌ Systemic handling practices causing adulteration
- ❌ Evidence that establishment lost control of its processes

**MOI Criteria Satisfied**:
- ✅ Isolated incident of mistreatment observed
- ✅ Single bird involved
- ✅ Does not represent ongoing systemic problem
- ✅ Documentation serves as warning/corrective discussion

**Regulatory Interpretation**: Per FSIS Directive 6110.1, *"An isolated instance does not represent a loss of process control and is to be documented in a mistreatment MOI, not an NR."*

**Outcome**: The MOI served to:
1. Formally document the observed mistreatment
2. Ensure immediate notification to establishment management
3. Create a record for tracking future incidents
4. Provide opportunity for establishment to take corrective action
5. Avoid formal violation while addressing animal welfare concern

**Note**: If similar incidents were observed repeatedly at this establishment, subsequent documentation could escalate to an NR, demonstrating a pattern that indicates loss of process control.

---

## Important Data Limitations

As noted in the USDA FSIS data documentation:

1. **Snapshot in Time**: The data reflects conditions at the time of inspection. Establishments may have implemented corrective actions since the data was collected.

2. **NR Eligibility**: Noncompliance records are only included if the NR regulations or description field is populated.

3. **Appeals Process**: Establishments may appeal inspection decisions per 9 CFR 306.5.

4. **MOI Objections**: Establishments may present objections to content within a Memorandum of Interview.

5. **Data Currency**: This archive dataset covers FY2024. Current conditions may differ from what is reflected in this historical data.

---

## Methodology

Data was analyzed using Python (pandas library) to:
1. Parse the Excel dataset structure
2. Identify and count formal violations (NRs) and MOIs
3. Search for the specific April 12, 2024 incident at establishment P2186
4. Extract detailed incident information

**Analysis Script**: `analyze_gcp_data.py`

---

## References

### Primary Sources
- **Primary Data Source**: `data/gcpArchiveFy2024.xlsx`
- **FSIS Directive 6110.1**: "Writing Noncompliance Records and Memoranda of Interview for Good Commercial Practices and Poultry Mistreatment"
- **FSIS Directive 6100.3**: "Ante-mortem and Post-mortem Poultry Inspection" (Section VII - Verification of Good Commercial Practices for Poultry)

### Regulations
- **9 CFR 381.65(b)**: Poultry slaughter in accordance with Good Commercial Practices (GCP)
- **9 CFR 381.90**: Carcasses showing evidence of having died from causes other than slaughter are considered adulterated
- **9 CFR 306.5**: Appeal process for inspection decisions
- **21 U.S.C. 453(g)(5)**: Poultry Products Inspection Act (PPIA) - adulteration definitions

### Additional Resources
- **Federal Register Notice**: "Treatment of Live Poultry Before Slaughter," 70 Fed. Reg. 56624 (September 28, 2005)
- **FSIS Directive 5000.1**: "Verifying an Establishment's Food Safety System"
- **FSIS Directive 8010.2**: "Investigative Methodology" (Chapter IV, Section III - MOI procedures)
- **USDA FSIS Data Documentation**: Available at https://www.fsis.usda.gov/

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-27 | 1.0 | Initial analysis of GCP FY2024 data and George's Foods incident |
| 2026-02-27 | 1.1 | Added comprehensive NR vs MOI framework based on FSIS Directive 6110.1; expanded regulatory analysis explaining why incident received MOI rather than formal NR; added detailed references |

