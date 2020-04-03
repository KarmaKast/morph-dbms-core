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

function condenseRelationClaim(
  relClaim: Structs.RelationClaim
): Structs.RelationClaimDense {
  return {
    To: relClaim.To.ID,
    Direction: relClaim.Direction,
    Relation: relClaim.Relation.ID,
  };
}

export function condenseEntity(entity: Structs.Entity): Structs.EntityDense {
  const res: Structs.EntityDense = {
    ID: entity.ID,
    Label: entity.Label,
    RelationClaims: Array.from(entity.RelationClaims.values()).map(
      condenseRelationClaim
    ),
  };
  if (entity.Data !== undefined) {
    res.Data = entity.Data;
  }
  //console.log(res);
  return res;
}

/**
 * ignores rel claims
 * @param entityCondensed
 */
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

interface RelationClaimDescribed
  extends Omit<Structs.RelationClaim, "To" | "Relation"> {
  To: string;
  Relation: string;
}

interface EntityDescribed extends Omit<Structs.Entity, "RelationClaims"> {
  RelationClaims: Array<RelationClaimDescribed>;
}

export function describe(
  entity: Structs.Entity,
  printToConsole = true,
  dataHieghtLimit = 10
): EntityDescribed {
  const log: EntityDescribed = {
    ID: entity.ID,
    Label: entity.Label,
    Data: entity.Data,
    RelationClaims: Array.from(entity.RelationClaims).map((relClaim) => {
      return {
        To: `{ ID: ${relClaim.To.ID}, Label: ${relClaim.To.Label} }`,
        Direction: relClaim.Direction,
        Relation: `{ ID: ${relClaim.Relation.ID}, Label: ${relClaim.Relation.Label} }`,
      };
    }),
  };
  if (printToConsole) console.log(JSON.stringify(log, undefined, 2));
  return log;
}
