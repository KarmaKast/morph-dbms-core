import { v1 } from "uuid";

import * as Structs from "./structs";

export function createNew(
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
  const relations: Structs.Collection["Relations"] = {};
  for (const relationClaim of entity.RelationClaims.values()) {
    if (!Object.values(knownRelations).includes(relationClaim.Relation)) {
      relations[relationClaim.Relation.ID] = relationClaim.Relation;
    }
  }
  return relations;
}

/**
 * populates relationclaims of a pass1 entity
 * @param condensedEntity
 * @param getEntityCallback
 * @param getRelationCallback
 */
export function populateEntityRelationClaims(
  condensedEntity: Structs.EntityDense,
  getEntityCallback: (entityID: Structs.Entity["ID"]) => Structs.Entity,
  getRelationCallback: (relationID: Structs.Relation["ID"]) => Structs.Relation
): Structs.Entity {
  const resEntity: Structs.Entity = getEntityCallback(condensedEntity.ID);
  condensedEntity.RelationClaims.forEach((relationClaim) => {
    resEntity.RelationClaims.add({
      To: getEntityCallback(relationClaim.To),
      Direction: relationClaim.Direction,
      Relation: getRelationCallback(relationClaim.Relation),
    });
  });
  return resEntity;
}

export function condenseEntity(entity: Structs.Entity): Structs.EntityDense {
  const res: Structs.EntityDense = {
    ID: entity.ID,
    Label: entity.Label,
    RelationClaims: Array.from(entity.RelationClaims.values()).map(
      (RelationClaim) => {
        return {
          To: RelationClaim.To.ID,
          Direction: RelationClaim.Direction,
          Relation: RelationClaim.Relation.ID,
        };
      }
    ),
  };
  if (entity.Data !== undefined) {
    res.Data = entity.Data;
  }
  //console.log(res);
  return res;
}

export function expandCondensedEntity(
  entityCondensed: Structs.EntityDense
): Structs.Entity {
  const res: Structs.Entity = {
    ID: entityCondensed.ID,
    Label: entityCondensed.Label,
    RelationClaims: new Set(),
  };
  if (entityCondensed.Data !== undefined) {
    res.Data = entityCondensed.Data;
  }
  return res;
}

export function describe(entity: Structs.Entity): void {
  console.log(
    "{\n  ID: ",
    entity.ID,
    "\n  Label: ",
    entity.Label,
    "\n  RelationClaims: ",
    entity.RelationClaims.size === 0 ? "{}" : ""
  );
  for (const relClaim of entity.RelationClaims) {
    console.log("  ", JSON.stringify(relClaim, undefined, 4));
  }
  console.log("}");
}
