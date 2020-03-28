/**
 * query database through collections and entities
 */

import * as Entity from "./entity";
import * as Collection from "./collection";
import * as Structs from "./structs";

// find entity with label

export class Query {
  Collection: Structs.Collection;
  constructor(Collection: Structs.Collection) {
    this.Collection = Collection;
  }
  hasLabel(Label: Structs.Entity["Label"]): Query {
    const newCollection: Structs.Collection = Collection.createNew(
      this.Collection.Label,
      undefined,
      undefined,
      this.Collection.ID
    );
    for (const entity of Object.values(this.Collection.Entities)) {
      console.log(entity);
      if (entity.Label === Label) {
        newCollection.Entities[entity.ID] = entity;
        Entity.getUniqueRelations(entity, this.Collection.Relations).forEach(
          (relation) => {
            newCollection.Relations.add(relation);
          }
        );
      }
    }
    return new Query(newCollection);
  }
}
