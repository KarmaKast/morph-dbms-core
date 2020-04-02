export interface Relation {
  ID: string;
  Label: string;
}

export enum Direction {
  FromSelf = "->",
  ToSelf = "<-",
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
  Data?: object;
}

export interface Collection {
  ID: string;
  Label: string | null;
  Entities: { [key: string]: Entity };
  Relations: { [key: string]: Relation };
}

// files

export interface RelationClaimDense {
  To: Entity["ID"];
  Relation: Relation["ID"];
  Direction: Direction;
}

export interface EntityDense {
  ID: Entity["ID"];
  Label: Entity["Label"];
  RelationClaims: Array<RelationClaimDense>;
  Data?: object;
}

export interface CollectionDense {
  ID: Collection["ID"];
  Label: Collection["Label"];
  Entities: Array<Entity["ID"]>;
  Relations: Array<Relation["ID"]>;
}
