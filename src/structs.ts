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
  Entities: {
    [key: string]: Entity;
  };
  Relations: Set<Relation>;
}

export interface CollectionFile {
  ID: Collection["ID"];
  Label: Collection["Label"];
  Entities: Array<Entity["ID"]>;
  Relations: Array<Relation["ID"]>;
}
