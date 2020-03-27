import { v1 } from "uuid";

import * as Structs from "./structs";

export function createEntity(
  ID?: Structs.Entity["ID"],
  Label?: Structs.Entity["Label"],
  RelationClaims?: Structs.Entity["RelationClaims"],
  Data?: Structs.Entity["Data"]
): Structs.Entity {
  const entity: Structs.Entity = {
    ID: ID === undefined ? v1() : ID,
    Label: Label === undefined ? null : Label,
    RelationClaims: RelationClaims === undefined ? new Set() : RelationClaims,
  };
  if (Data !== undefined) {
    entity.Data = Data;
  }
  return entity;
}

export function createRelation(
  Label: Structs.Relation["Label"],
  ID?: Structs.Relation["ID"]
): Structs.Relation {
  const relation: Structs.Relation = {
    ID: ID === undefined ? v1() : ID,
    Label: Label,
  };
  return relation;
}

export function claimRelation(
  relation: Structs.Relation,
  direction: Structs.Direction,
  ownerEntity: Structs.Entity,
  targetEntity: Structs.Entity
): void {
  const claim: Structs.RelationClaim = {
    Direction: direction,
    Relation: relation,
    To: targetEntity,
  };
  ownerEntity.RelationClaims.add(claim);
}

export function getUniqueRelations(
  entity: Structs.Entity,
  knownRelations: Structs.Collection["Relations"]
): Structs.Collection["Relations"] {
  const relations: Structs.Collection["Relations"] = [];

  for (const relationClaim of entity.RelationClaims) {
    if (!knownRelations.includes(relationClaim.Relation)) {
      relations.push(relationClaim.Relation);
    }
  }
  return relations;
}
