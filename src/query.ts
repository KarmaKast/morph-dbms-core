/**
 * query database through collections and entities
 */

import * as Entity from "./entity";
import * as Collection from "./collection";
import * as Structs from "./structs";

// find entity with label

export class QueryEntity {
  entity: Structs.Entity;
  constructor(entity: Structs.Entity) {
    this.entity = entity;
  }
  hasRelationClaim(
    relation: Structs.Relation,
    direction: Structs.Direction
  ): boolean {
    for (const relClaim of this.entity.RelationClaims) {
      if (relation === relClaim.Relation && direction === relClaim.Direction) {
        return true;
      } else {
        return false;
      }
    }
    return false;
  }
}

export class QueryCollection {
  collection: Structs.Collection;
  constructor(collection: Structs.Collection) {
    this.collection = collection;
  }
  hasLabel(label: Structs.Entity["Label"]): QueryCollection {
    const newCollection: Structs.Collection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Object.values(this.collection.Entities)) {
      if (entity.Label === label) {
        newCollection.Entities[entity.ID] = entity;
        Object.values(
          Entity.getUniqueRelations(entity, this.collection.Relations)
        ).forEach((relation) => {
          newCollection.Relations[relation.ID] = relation;
        });
      }
    }
    return new QueryCollection(newCollection);
  }
  hasRelationClaim(
    relation: Structs.Relation,
    direction: Structs.Direction
  ): QueryCollection {
    const newCollection: Structs.Collection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Object.values(this.collection.Entities)) {
      if (new QueryEntity(entity).hasRelationClaim(relation, direction)) {
        this.collection.Entities[entity.ID] = entity;
      }
    }
    return new QueryCollection(newCollection);
  }
}
