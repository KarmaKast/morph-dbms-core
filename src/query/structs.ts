import { Structs } from "..";

export abstract class QueryBase {
  collectionID: Structs.Collection["ID"];
  constructor(collectionID: Structs.Collection["ID"]) {
    this.collectionID = collectionID;
  }
  abstract branchOut(callback: (QueryObj: this) => void | this[]): this;
  abstract branchIn(callback: (QueryObj: this) => void | this[]): this;

  // doing: queries

  abstract hasLabel(label: string): this;
  abstract hasRelationClaim(
    relationID: Structs.Relation["ID"],
    direction: Structs.Direction,
    to?: Structs.Entity
  ): this;
  abstract usesRelation(
    relationLabel: Structs.Relation["Label"],
    relationID?: Structs.Relation["ID"],
    relation?: Structs.Relation
  ): this;
  abstract filterData(properties?: any[] | null): this;
}

interface HasLabelQuery {
  hasLabelParams: Parameters<QueryBase["hasLabel"]>;
}
interface HasRelationClaimQuery {
  hasRelationClaimParams: Parameters<QueryBase["hasRelationClaim"]>;
}
interface UsesRelationQuery {
  usesRelationParams: Parameters<QueryBase["usesRelation"]>;
}
interface FilterDataQuery {
  filterDataParams: Parameters<QueryBase["filterData"]>;
}
interface BranchOutQuery<L> {
  branchOutTasks: void | L[];
}
interface BranchInQuery<L> {
  branchInTasks: void | L[];
}
export interface MetaData {
  collectionID: Structs.Collection["ID"];
  collection?: Structs.Collection;
  dataBasePath: string;
}
export type queriesUnion<V> =
  | MetaData
  | HasLabelQuery
  | HasRelationClaimQuery
  | UsesRelationQuery
  | FilterDataQuery
  | BranchOutQuery<V>
  | BranchInQuery<V>;

export class QueryTypeTests {
  static isHasLabelquery<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is HasLabelQuery {
    return (parsedQuery as HasLabelQuery).hasLabelParams !== undefined;
  }
  static isHasRelationClaimQuery<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is HasRelationClaimQuery {
    return (
      (parsedQuery as HasRelationClaimQuery).hasRelationClaimParams !==
      undefined
    );
  }
  static isUsesRelationQuery<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is UsesRelationQuery {
    return (parsedQuery as UsesRelationQuery).usesRelationParams !== undefined;
  }
  static isFilterDataQuery<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is FilterDataQuery {
    return (parsedQuery as FilterDataQuery).filterDataParams !== undefined;
  }
  static isBranchOutQuery<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is BranchOutQuery<R> {
    return (parsedQuery as BranchOutQuery<R>).branchOutTasks !== undefined;
  }
  static isCollection<R>(
    parsedQuery: queriesUnion<R>
  ): parsedQuery is MetaData {
    return (parsedQuery as MetaData).collectionID !== undefined;
  }
}
