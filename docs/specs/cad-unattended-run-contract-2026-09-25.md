# CAD unattended-run contract (2026-09-25)

**Status: documentation gap analysis and test recipe. Nothing was run on the host; no unattended
capability is demonstrated.** The implementation home stays `500ft/engineering-audit` — this repo
does **not** gain a second automation framework. Scope today is the *contract*; qualifying it needs
host evidence.

**The distinction this document exists to protect:** *documented API behaviour* ≠ *host-proven
capability*. Everything below is the former until a clean run and controlled failure cases exist.

## What is already true (do not re-derive)

- `docs/host_setup.md` says to **discover the logged-in desktop session and its owner**. Session ID
  `1` is the **observed** value on the reference host — **not a universal requirement**, and
  **autologon is not implied** by needing an interactive session. Earlier notes in this project
  overstated both; corrected here.
- `cadloop/worker.py` already **refuses to proceed when a SOLIDWORKS process is running**, so it
  never takes ownership of someone else's session. **Preserve that behaviour.**

## Dialog suppression — what is actually documented

Verified as **operation-specific** options, not a global "no dialogs" switch:

| Setting | Applies to | Source |
|---|---|---|
| `swOpenDocOptions_Silent` | document **open** | [swOpenDocOptions_e](https://help.solidworks.com/2017/english/api/swconst/solidworks.interop.swconst~solidworks.interop.swconst.swopendocoptions_e.html) |
| `swSaveAsOptions_Silent` | applicable **save/export** calls | [IModelDocExtension.SaveAs2](https://help.solidworks.com/2025/english/api/sldworksapi/solidworks.interop.sldworks~solidworks.interop.sldworks.imodeldocextension~saveas2.html) |

**These do not guarantee suppression of every modal dialog.** Visibility flags and
`UserControlBackground` are **not** proof of suppression either. On the installed version, verify:
the method overload, the export format, the **returned status / error / warning values**, and the
**artifact on disk**.

> **The safe form of "I never click anything" is: silent options at the API level, plus an oracle
> that refuses the part on a number mismatch — never blanket auto-accept of unknown dialogs.**
> Suppression removes the only interactive warning, which is exactly why the numeric check stops
> being optional. The briefing records three cases in one week where a job reported success while
> producing wrong geometry; a screenshot passed every time.

## The contract

1. **Preflight** the actual interactive session and account, installed version and license,
   templates, paths, and a free output location. A missing prerequisite yields a **specific blocked
   result** — never a request for an arbitrary click.
2. **Isolated job directory**; own only the process launched for that job. **Never dismiss an
   unknown dialog blindly, and never kill an unrelated interactive process.**
3. **Log** stage, deadline, job and process identity, return codes, and artifact paths.
4. **Outer watchdog independent of the COM call.** A blocked synchronous call **cannot** be rescued
   by a timeout implemented inside that same call's thread.
5. On timeout or an unexpected dialog: record diagnostics, then stop or recover **only the
   job-owned process** under the documented policy. **Success is never inferred from a launch
   returning.**
6. After save/export: inspect non-empty files, run the **geometry oracle**, check required features,
   **re-drive a parameter**, and **re-import the STEP**. Report `unverified` and `mismatched` as
   distinct outcomes — neither is a pass.
7. **Qualification (not done today):** one clean successful run plus controlled failure cases —
   missing template/path, occupied output, an existing user process, an invalid session, a blocked
   worker, and an export failure. Startup/license failures need a **controlled test environment**;
   do not disrupt a working installation to simulate them.

## Explicitly untested

Every row of the contract. No host was contacted this session. **Unattended no-click operation
remains unverified until host evidence exists** — and this document must not become the reason the
pilot never starts.

*Authority:* `500ft/engineering-audit` → `docs/cad_agent_briefing.md`, `docs/host_setup.md`,
`docs/solidworks_api_findings.md`, `cadloop/worker.py`. Also
[Interactive Services](https://learn.microsoft.com/en-us/windows/win32/services/interactive-services).
