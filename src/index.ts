export * as Entity from "./entity";
export * as Collection from "./collection";
export * as Query from "./query";
export * as Structs from "./structs";
export { Direction } from "./structs";

import { v1 } from "uuid";
import * as Structs from "./structs";
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
