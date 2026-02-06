import yaml
from core.ui import header, section, log, Timer


class Orchestrator:
    def __init__(self, planner, researcher, analyst, writer, fact_checker, memory):
        self.planner = planner
        self.researcher = researcher
        self.analyst = analyst
        self.writer = writer
        self.fact_checker = fact_checker
        self.memory = memory

        with open("config/research.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)["research"]

    def run(self):
        header()

        # ────────────────────────
        # 🧠 PLANNER
        # ────────────────────────
        section("🧠 PLANNER")
        log(f'Query: "{self.memory.state.query}"', "cyan")

        with Timer() as t:
            plan = self.planner.create_plan(self.memory.state.query)

        if not plan:
            return {
                "status": "failed",
                "error": "Planner produced no research steps",
            }

        self.memory.add_plan(plan)

        for step in plan:
            log(f"• {step}", "green")
        log(f"Completed in {t.elapsed:.2f}s", "dim")

        draft = None  # 🔑 ensure defined

        # ────────────────────────
        # 🔁 ITERATIVE PIPELINE
        # ────────────────────────
        for iteration in range(1, self.config["max_iterations"] + 1):
            log(f"\nIteration {iteration}/{self.config['max_iterations']}", "bold cyan")

            # ────────────────────────
            # 🔍 RESEARCHER
            # ────────────────────────
            section("🔍 RESEARCHER")
            try:
                with Timer() as t:
                    sources = self.researcher.collect_sources(plan)
            except Exception as e:
                log(f"Research failed: {e}", "red")
                return {
                    "status": "failed",
                    "error": "Research phase failed",
                }

            log(f"Collected {len(sources)} sources", "green")
            log(f"Time: {t.elapsed:.2f}s", "dim")

            for s in sources:
                self.memory.add_source(s)

            # ────────────────────────
            # 📊 ANALYST
            # ────────────────────────
            section("📊 ANALYST")
            claims = self.analyst.extract_claims(sources)
            self.memory.state.claims = claims
            log(f"Extracted claims: {len(claims)}", "green")

            if not claims:
                log("No claims extracted, retrying iteration", "yellow")
                continue

            # ────────────────────────
            # ✍️ WRITER
            # ────────────────────────
            section("✍️ WRITER")
            with Timer() as t:
                draft = self.writer.write(self.memory.state)

            log(f"Draft completed in {t.elapsed:.2f}s", "green")

            # attach claims explicitly
            draft["claims"] = [c.__dict__ for c in claims]

            # ────────────────────────
            # ✅ FACT CHECKER
            # ────────────────────────
            section("✅ FACT CHECKER")
            result = self.fact_checker.verify(draft, self.memory.state)

            if result.get("status") == "approved":
                log("STATUS: APPROVED", "bold green")
                return result

            log("Fact check failed, retrying…", "yellow")

        # ────────────────────────
        # ⚠ PARTIAL RESULT
        # ────────────────────────
        log("STATUS: PARTIAL RESULT (max iterations reached)", "bold yellow")

        return {
            "status": "partial",
            "message": "Confidence threshold not met after retries",
            "draft": draft,
        }
