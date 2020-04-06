export interface Relation {
  ID: string;
  Label: string;
}

export enum Direction {
  SelfToTarget = "->",
  TargetToSelf = "<-",
}

export interface RelationClaim {
  To: Entity;
  Relation: Relation;
  Direction: Direction;
}

export interface Entity {
  ID: string;
  Label: string | null;
  RelationClaims: Set<RelationClaim>;
  Data?: Map<string, unknown>;
}

export interface Collection {
  ID: string;
  Label: string | null;
  Entities: Map<Entity["ID"], Entity>;
  Relations: Map<Relation["ID"], Relation>;
}

// files

export interface RelationClaimDense
  extends Omit<RelationClaim, "To" | "Relation"> {
  To: Entity["ID"];
  Relation: Relation["ID"];
}

export interface EntityDense extends Omit<Entity, "RelationClaims"> {
  RelationClaims: Array<RelationClaimDense>;
}

export type CondensedEntities = Map<string, EntityDense>;

export interface CollectionDense
  extends Omit<Collection, "Entities" | "Relations"> {
  Entities: Array<Entity["ID"]>;
  Relations: Array<Relation["ID"]>;
}
