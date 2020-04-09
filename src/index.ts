export * as Entity from "./entity";
export * as Collection from "./collection";
export * as QueryRunner from "./query";
export * as Structs from "./structs";
export * as Files from "./files";
export { Direction } from "./structs";

export * as ExperimentalQuery from "./query/index";

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
