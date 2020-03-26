import { v1 } from "uuid";

import * as structs from "./structs";

export function createEntity(
  ID?: structs.Entity["ID"],
  Label?: structs.Entity["Label"],
  RelationClaims?: structs.Entity["RelationClaims"],
  Data?: structs.Entity["Data"]
): structs.Entity {
  const entity: structs.Entity = {
    ID: ID === undefined ? v1() : ID,
    Label: Label === undefined ? null : Label,
    RelationClaims: RelationClaims === undefined ? [] : RelationClaims,
    Data: Data === undefined ? {} : Data,
  };
  return entity;
}
