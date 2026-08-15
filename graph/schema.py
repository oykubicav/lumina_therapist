"""Uniqueness constraints — idempotent DDL.

Constraint aynı zamanda index görevi görür → MERGE + MATCH hızlanır.
"""

def create_schema(session):
    """Her node label'ı için unique id constraint."""
    session.run("CREATE CONSTRAINT card_id IF NOT EXISTS FOR (c:Card) REQUIRE c.id IS UNIQUE")
    session.run("CREATE CONSTRAINT module_id IF NOT EXISTS FOR (m:Module) REQUIRE m.id IS UNIQUE")
    session.run("CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE")
    session.run("CREATE CONSTRAINT conceptgroup_id IF NOT EXISTS FOR (g:ConceptGroup) REQUIRE g.id IS UNIQUE")
  
    session.run("CREATE CONSTRAINT source_id IF NOT EXISTS FOR (s:Source) REQUIRE s.id IS UNIQUE")

    session.run("CREATE CONSTRAINT technique_id IF NOT EXISTS FOR (t:Technique) REQUIRE t.id IS UNIQUE")