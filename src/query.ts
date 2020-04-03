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
  hasLabel(label: Structs.Entity["Label"]): QueryCollection {
    const newCollection = Collection.createNew(
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
    direction: Structs.Direction,
    to?: Structs.Entity
  ): QueryCollection {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    for (const entity of Object.values(this.collection.Entities)) {
      if (new QueryEntity(entity).hasRelationClaim(relation, direction, to)) {
        newCollection.Entities[entity.ID] = entity;
        newCollection.Relations[relation.ID] = relation;
      }
    }
    return new QueryCollection(newCollection);
  }
  usesRelation(
    relationLabel: Structs.Relation["Label"],
    relation?: Structs.Relation,
    relationID?: Structs.Relation["ID"]
  ): QueryCollection {
    const newCollection = Collection.createNew(
      this.collection.Label,
      undefined,
      undefined,
      this.collection.ID
    );
    if (relation) {
      if (Object.values(this.collection.Relations).includes(relation)) {
        newCollection.Relations[relation.ID] = relation;
      }
    } else if (relationID) {
      if (Object.keys(this.collection.Relations).includes(relationID)) {
        newCollection.Relations[relationID] = this.collection.Relations[
          relationID
        ];
      }
    } else {
      const filteredRelations = Object.values(this.collection.Relations).filter(
        (relation_) => relation_.Label === relationLabel
      );
      if (filteredRelations.length === 1) {
        newCollection.Relations[
          filteredRelations[0].ID
        ] = this.collection.Relations[filteredRelations[0].ID];
      }
    }

    for (const entity of Object.values(this.collection.Entities)) {
      if (
        new QueryEntity(entity).usesRelation(
          relationLabel,
          relation,
          relationID
        )
      ) {
        newCollection.Entities[entity.ID] = entity;
      }
    }
    return new QueryCollection(newCollection);
  }
  filterData(properties?: Array<string> | null) {
    if (properties === undefined) return new QueryCollection(this.collection);
  }
}
