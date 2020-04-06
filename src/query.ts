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
    direction: Structs.Direction,
    to?: Structs.Entity
  ): boolean {
    for (const relClaim of this.entity.RelationClaims) {
      if (
        relation.ID === relClaim.Relation.ID &&
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

export class QueryCollection {
  collection: Structs.Collection;

  constructor(collection: Structs.Collection) {
    this.collection = collection;
  }

  doSomething = (
    callback: (QueryObj: QueryCollection) => void
  ): QueryCollection => {
    callback(this);
    return this;
  };

  // queries

  hasLabel(label: Structs.Entity["Label"]): QueryCollection {
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
    return new QueryCollection(newCollection);
  }

  hasRelationClaim(
    relation: Structs.Relation,
    direction: Structs.Direction,
    to?: Structs.Entity
  ): QueryCollection {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Array.from(this.collection.Entities.values())) {
      if (new QueryEntity(entity).hasRelationClaim(relation, direction, to)) {
        newCollection.Entities.set(entity.ID, entity);
        newCollection.Relations.set(relation.ID, relation);
      }
    }
    return new QueryCollection(newCollection);
  }

  usesRelation(
    relationLabel: Structs.Relation["Label"],
    relationID?: Structs.Relation["ID"],
    relation?: Structs.Relation
  ): QueryCollection {
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
    return new QueryCollection(newCollection);
  }

  filterData(properties?: Array<string> | null): QueryCollection {
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
    return new QueryCollection(newCollection);
  }
}
