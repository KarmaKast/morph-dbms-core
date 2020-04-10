import { Structs } from "..";
import { QueryBase, queriesUnion, MetaData } from "./structs";
import { cloneDeep } from "lodash";

export class QueryParser extends QueryBase {
  /*encodedQuery: [
    "hasLabel" | "hasRelationClaim" | "usesRelation" | "filterData",
    any[]
  ][];*/
  encodedQuery: queriesUnion<QueryParser>[];
  constructor(
    encodedQuery?: queriesUnion<QueryParser>[],
    collectionID?: Structs.Collection["ID"],
    dataBasePath?: string
  ) {
    if (encodedQuery) {
      const encodedQueryCopy = cloneDeep(encodedQuery);
      const metaData = encodedQueryCopy[0] as MetaData;
      super(metaData.collectionID);
      this.encodedQuery = encodedQueryCopy;
    } else if (collectionID && dataBasePath) {
      super(collectionID);
      this.encodedQuery = [
        { collectionID: collectionID, dataBasePath: dataBasePath },
      ];
    } else throw new Error("later");
  }
  branchOut(callback: (QueryObj: this) => void | this[]): this {
    const metaData = this.encodedQuery[0] as MetaData;
    this.encodedQuery.push({
      branchOutTasks: callback(
        new QueryParser(cloneDeep(this.encodedQuery)) as this
      ),
    });
    return this;
  }
  branchIn(callback: (QueryObj: this) => void | this[]): this {
    const nextQuery = new QueryParser(this.encodedQuery);
    nextQuery.encodedQuery.push({
      branchInTasks: callback(this),
    });
    return nextQuery as this;
  }

  // doing: queries

  hasLabel(label: string): this {
    const nextQuery = new QueryParser(this.encodedQuery);
    nextQuery.encodedQuery.push({ hasLabelParams: [label] });
    return nextQuery as this;
  }
  hasRelationClaim(
    relationID: Structs.Relation["ID"],
    direction: Structs.Direction,
    to?: Structs.Entity
  ): this {
    const nextQuery = new QueryParser(this.encodedQuery);
    nextQuery.encodedQuery.push({
      hasRelationClaimParams: [relationID, direction, to],
    });
    return nextQuery as this;
  }
  usesRelation(
    relationLabel: Structs.Relation["Label"],
    relationID?: Structs.Relation["ID"],
    relation?: Structs.Relation
  ): this {
    const nextQuery = new QueryParser(this.encodedQuery);
    nextQuery.encodedQuery.push({
      usesRelationParams: [relationLabel, relationID, relation],
    });
    return nextQuery as this;
  }
  filterData(properties?: any[] | null): this {
    const nextQuery = new QueryParser(this.encodedQuery);
    nextQuery.encodedQuery.push({
      filterDataParams: [properties],
    });
    return nextQuery as this;
  }
}
