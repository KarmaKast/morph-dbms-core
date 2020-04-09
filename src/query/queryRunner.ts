/**
 * query database through collections and entities
 */

import { Structs, Collection, Entity, Files } from "..";

import { QueryBase, QueryTypeTests, queriesUnion } from "./structs";
import { QueryParser } from "./parser";

// find entity with label

export class QueryEntity {
  entity: Structs.Entity;
  constructor(entity: Structs.Entity) {
    this.entity = entity;
  }
  hasRelationClaim(
    relationID: Structs.Relation["ID"],
    direction: Structs.Direction,
    to?: Structs.Entity
  ): boolean {
    for (const relClaim of this.entity.RelationClaims) {
      if (
        relationID === relClaim.Relation.ID &&
        direction === relClaim.Direction &&
        (to === undefined || to.ID === relClaim.To.ID)
      ) {
        return true;
      } else {
        return false;
      }
    }
    return false;
  }
  usesRelation(
    relationLabel: Structs.Relation["Label"],
    relation?: Structs.Relation,
    relationID?: Structs.Relation["ID"]
  ): boolean {
    for (const relClaim of this.entity.RelationClaims) {
      if (relation) {
        if (relation === relClaim.Relation) {
          return true;
        } else {
          return false;
        }
      } else if (relationID) {
        if (relationID === relClaim.Relation.ID) {
          return true;
        } else {
          return false;
        }
      } else {
        if (relationLabel === relClaim.Relation.Label) {
          return true;
        } else {
          return false;
        }
      }
    }
    return false;
  }
}

export class QueryCollection extends QueryBase {
  collection: Structs.Collection;

  constructor(
    collection: Structs.Collection,
    collectionID: Structs.Collection["ID"]
  ) {
    super(collectionID);
    this.collection = collection;
  }

  branchOut(callback: (QueryObj: this) => void | this[]): this {
    callback(new QueryCollection(this.collection, this.collectionID) as this);
    return this;
  }

  branchIn(callback: (QueryObj: this) => void | this[]): this {
    const QueryCollectionObjects = callback(this);
    if (QueryCollectionObjects && QueryCollectionObjects.length > 0) {
      if (QueryCollectionObjects.length > 1) {
        const collections = QueryCollectionObjects.map(
          (value) => value.collection
        );
        Collection.merge(collections[0], collections.slice(1));
        return new QueryCollection(collections[0], collections[0].ID) as this;
      } else {
        return QueryCollectionObjects[0] as this;
      }
    } else {
      return this;
    }
  }

  // queries

  hasLabel(label: Structs.Entity["Label"]): this {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Array.from(this.collection.Entities.values())) {
      if (entity.Label === label) {
        newCollection.Entities.set(entity.ID, entity);
        Array.from(
          Entity.getUniqueRelations(entity, this.collection.Relations).values()
        ).forEach((relation) => {
          newCollection.Relations.set(relation.ID, relation);
        });
      }
    }
    return new QueryCollection(newCollection, newCollection.ID) as this;
  }

  hasRelationClaim(
    relationID: Structs.Relation["ID"],
    direction: Structs.Direction,
    to?: Structs.Entity
  ): this {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Array.from(this.collection.Entities.values())) {
      if (new QueryEntity(entity).hasRelationClaim(relationID, direction, to)) {
        newCollection.Entities.set(entity.ID, entity);
        const relation = this.collection.Relations.get(relationID);
        if (relation) {
          newCollection.Relations.set(relationID, relation);
        }
      }
    }
    return new QueryCollection(newCollection, newCollection.ID) as this;
  }

  usesRelation(
    relationLabel: Structs.Relation["Label"],
    relationID?: Structs.Relation["ID"],
    relation?: Structs.Relation
  ): this {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    if (relation) {
      if (Array.from(this.collection.Relations.values()).includes(relation)) {
        newCollection.Relations.set(relation.ID, relation);
      }
    } else if (relationID) {
      const resRelaton = this.collection.Relations.get(relationID);
      if (resRelaton) {
        newCollection.Relations.set(relationID, resRelaton);
      }
    } else {
      const filteredRelations = Array.from(
        this.collection.Relations.values()
      ).filter((relation_) => relation_.Label === relationLabel);
      if (filteredRelations.length === 1) {
        const resRelation = this.collection.Relations.get(
          filteredRelations[0].ID
        );
        if (resRelation) {
          newCollection.Relations.set(filteredRelations[0].ID, resRelation);
        }
      }
    }

    for (const entity of Array.from(this.collection.Entities.values())) {
      if (
        new QueryEntity(entity).usesRelation(
          relationLabel,
          relation,
          relationID
        )
      ) {
        newCollection.Entities.set(entity.ID, entity);
      }
    }
    return new QueryCollection(newCollection, newCollection.ID) as this;
  }

  filterData(properties?: Array<string> | null): this {
    const newCollection = Collection.createNew(
      this.collection.Label,
      this.collection.Entities,
      this.collection.Relations,
      this.collection.ID
    );
    if (properties === null || (properties && properties.length === 0)) {
      Array.from(newCollection.Entities.values()).map((entity) => {
        delete entity.Data;
      });
    } else if (properties && properties.length !== 0) {
      Array.from(newCollection.Entities.values()).map((entity) => {
        if (entity.Data !== undefined) {
          const entityCopy = entity;
          entity.Data = new Map();
          properties.map((propertyID) => {
            if (entity.Data && entityCopy.Data) {
              const property = entityCopy.Data.get(propertyID);
              if (property) entity.Data.set(propertyID, property);
            }
            return propertyID;
          });
        }
      });
    }
    return new QueryCollection(newCollection, newCollection.ID) as this;
  }
}

export function runParsedQuery(
  encodedQuery: QueryParser["encodedQuery"],
  dataBasePath: string,
  ...branchOut: ((queryObjCollection: Structs.Collection) => void)[]
): QueryCollection {
  const MetaData = encodedQuery[0];
  if (QueryTypeTests.isMetaData(MetaData)) {
    MetaData.collection = Files.readCollection(
      MetaData.collectionID,
      dataBasePath
    );
    let queryObj = new QueryCollection(
      MetaData.collection,
      MetaData.collection.ID
    );
    encodedQuery.slice(1).forEach((parsedQuery) => {
      const compromise = parsedQuery;
      if (QueryTypeTests.isHasLabelquery(compromise)) {
        queryObj = queryObj.hasLabel(...compromise.hasLabelParams);
      } else if (QueryTypeTests.isHasRelationClaimQuery(compromise)) {
        queryObj = queryObj.hasRelationClaim(
          ...compromise.hasRelationClaimParams
        );
      } else if (QueryTypeTests.isUsesRelationQuery(compromise)) {
        queryObj = queryObj.usesRelation(...compromise.usesRelationParams);
      } else if (QueryTypeTests.isFilterDataQuery(compromise)) {
        queryObj = queryObj.filterData(...compromise.filterDataParams);
      } else if (QueryTypeTests.isBranchOutQuery(compromise)) {
        console.log(compromise.branchOutTasks);
        // todo: .
        queryObj = queryObj.branchOut(() => {
          if (compromise.branchOutTasks)
            return compromise.branchOutTasks.map((task) => {
              return runParsedQuery(task.encodedQuery, dataBasePath);
            });
        });
      } else if (QueryTypeTests.isBranchInQuery(compromise)) {
        // todo: run the branch in tasks and then merge the resulting QueryCollection objects
        if (compromise.branchInTasks) {
          queryObj = queryObj.branchIn(() => {
            if (compromise.branchInTasks)
              return compromise.branchInTasks.map((task) => {
                return runParsedQuery(task.encodedQuery, dataBasePath);
              });
          });
        }
      }
    });

    return queryObj;
  } else throw new Error("this shouldn't have happened");
}
