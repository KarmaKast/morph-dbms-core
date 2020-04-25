import { v1 } from "uuid";

import { Structs } from ".";

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
  claimantEntity: Structs.Entity,
  targetEntity: Structs.Entity
): void {
  const claim: Structs.RelationClaim = {
    Direction: direction,
    Relation: relation,
    To: targetEntity,
  };
  claimantEntity.RelationClaims.add(claim);
}

/**
 * drops all relation claims related to a target and return true if claimantEntity had a relClaim towards Target
 * @param claimantEntity
 * @param targetEntityID
 */
export function dropRelationClaimsTo(
  claimantEntity: Structs.Entity,
  targetEntityID: Structs.Entity["ID"]
): boolean {
  let res = false;
  claimantEntity.RelationClaims.forEach((relClaim) => {
    if (relClaim.To.ID === targetEntityID) {
      res = true;
      claimantEntity.RelationClaims.delete(relClaim);
    }
  });
  return res;
}

export function getUniqueRelations(
  entity: Structs.Entity,
  knownRelations: Structs.Collection["Relations"]
): Structs.Collection["Relations"] {
  const relations: Structs.Collection["Relations"] = new Map();
  for (const relationClaim of entity.RelationClaims.values()) {
    if (!Object.values(knownRelations).includes(relationClaim.Relation)) {
      relations.set(relationClaim.Relation.ID, relationClaim.Relation);
    }
  }
  return relations;
}

/**
 * populates relationclaims of a pass1 entity
 */
export function populateEntityRelationClaims(
  condensedEntity: Structs.EntityDense,
  getEntityCallback: (entityID: Structs.Entity["ID"]) => Structs.Entity | null,
  getRelationCallback: (
    relationID: Structs.Relation["ID"]
  ) => Structs.Relation | null
): Structs.Entity {
  const resEntity = getEntityCallback(condensedEntity.ID);
  if (resEntity) {
    condensedEntity.RelationClaims.forEach((relationClaim) => {
      const toEntity = getEntityCallback(relationClaim.To);
      const relation = getRelationCallback(relationClaim.Relation);
      if (toEntity && relation)
        resEntity.RelationClaims.add({
          To: toEntity,
          Direction: relationClaim.Direction,
          Relation: relation,
        });
    });
    return resEntity;
  } else throw new Error("idk");
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
    res.Data = {};
    entity.Data.forEach((value, key) => {
      if (res.Data) res.Data[key] = value;
    });
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
    res.Data = new Map(Object.entries(entityCondensed.Data));
  }
  return res;
}

interface RelationClaimDescribed
  extends Omit<Structs.RelationClaim, "To" | "Relation"> {
  To: string;
  Relation: string;
}

interface EntityDescribed
  extends Omit<Structs.Entity, "RelationClaims" | "Data"> {
  RelationClaims: RelationClaimDescribed[];
  Data?: Record<string, unknown>;
}

export function describe(
  entity: Structs.Entity,
  printToConsole = true,
  noData = false,
  dataHeightLimit = 10
): EntityDescribed {
  const log: EntityDescribed = {
    ID: entity.ID,
    Label: entity.Label,
    RelationClaims: Array.from(entity.RelationClaims.values()).map(
      (relClaim) => {
        return {
          To: `{ ID: '${relClaim.To.ID}', Label: '${relClaim.To.Label}' }`,
          Direction: relClaim.Direction,
          Relation: `{ ID: '${relClaim.Relation.ID}', Label: '${relClaim.Relation.Label}' }`,
        };
      }
    ),
  };
  if (!noData && entity.Data) {
    log.Data = Object.fromEntries(entity.Data.entries());
  }
  if (printToConsole) {
    console.log(
      "----------------------------Entity----------------------------"
    );
    console.log(JSON.stringify(log, undefined, 2));
    console.log(
      "--------------------------------------------------------------"
    );
  }
  return log;
}
