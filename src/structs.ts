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
  Data?: Record<string, object>;
}

export interface Collection {
  ID: string;
  Label: string | null;
  Entities: Record<string, Entity>;
  Relations: Record<string, Relation>;
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

export interface CollectionDense
  extends Omit<Collection, "Entities" | "Relations"> {
  Entities: Array<Entity["ID"]>;
  Relations: Array<Relation["ID"]>;
}
