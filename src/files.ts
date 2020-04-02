import * as Structs from "./structs";
import * as Entity from "./entity";
import * as fs from "fs";
import * as path from "path";
import { Collection } from ".";

export function initDatabase(
  dataBasePath: string,
  mode: "init" | "reset" = "init"
): Promise<void> {
  function init(): void {
    fs.mkdirSync(dataBasePath, { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Entities"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Collections"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Relations"), { recursive: true });
  }
  switch (mode) {
    case "reset":
      // remove the database folder completely
      if (fs.existsSync(dataBasePath)) {
        fs.rmdirSync(dataBasePath, { recursive: true });
      }
      init();
      return new Promise((resolve) => {
        console.log("reset done");
        resolve();
      });

      break;
    case "init":
      // check database folder integrity
      if (!fs.existsSync(dataBasePath)) {
        init();
      }
      break;
  }
  return new Promise((resolve, reject) => {
    reject("idk");
  });
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Entities", entity.ID + ".entity.json")
    ),
    JSON.stringify(Entity.condenseEntity(entity)),
    { flag: "w+" },
    () => {
      //
    }
  );
}

export function writeRelation(
  relation: Structs.Relation,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Relations", relation.ID + ".relation.json")
    ),
    JSON.stringify(relation),
    { flag: "w+" },
    () => {
      //
    }
  );
}

function mapCollectionToFile(
  collection: Structs.Collection
): Structs.CollectionDense {
  const res: Structs.CollectionDense = {
    ID: collection.ID,
    Label: collection.Label,
    Entities: Object.keys(collection.Entities).map((key) => {
      return collection.Entities[key].ID;
    }),
    Relations: Object.keys(collection.Relations).map((key) => {
      return collection.Relations[key].ID;
    }),
  };
  //console.log(res);
  return res;
}

export function writeCollection(
  collection: Structs.Collection,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Collections", collection.ID + ".collection.json")
    ),
    JSON.stringify(Collection.condenseCollection(collection)),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
  for (const entityID in collection.Entities) {
    writeEntity(collection.Entities[entityID], dataBasePath);
  }
  for (const relationID in collection.Relations) {
    writeRelation(collection.Relations[relationID], dataBasePath);
  }
}

// doing: reading from file

/**
 * pass 1: creates entity ignoring the relation claims
 */
export function readEntityPass1(
  dataBasePath: string,
  entityID: Structs.Entity["ID"]
): [Structs.Entity, Structs.EntityDense] {
  const resEntityFile: Structs.EntityDense = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Entities", entityID + ".entity.json")
      )
      .toString()
  );
  const resEntity: Structs.Entity = Entity.expandCondensedEntity(resEntityFile);
  return [resEntity, resEntityFile];
}

export function readEntityPass2(
  entityFile: Structs.EntityDense,
  getEntityCallback: (entityID: Structs.Entity["ID"]) => Structs.Entity,
  getRelationCallback: (relationID: Structs.Relation["ID"]) => Structs.Relation
): Structs.Entity {
  const resEntity: Structs.Entity = getEntityCallback(entityFile.ID);
  entityFile.RelationClaims.forEach((relationClaim) => {
    resEntity.RelationClaims.add({
      To: getEntityCallback(relationClaim.To),
      Direction: relationClaim.Direction,
      Relation: getRelationCallback(relationClaim.Relation),
    });
  });
  return resEntity;
}

export function readRelation(
  relationID: Structs.Relation["ID"],
  dataBasePath: string
): Structs.Relation {
  const relation: Structs.Relation = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Relations", relationID + ".relation.json")
      )
      .toString()
  );
  return relation;
}

function mapCollectionFromFile(
  collectionFile: Structs.CollectionDense,
  dataBasePath: string
): Structs.Collection {
  const relations: Structs.Collection["Relations"] = {};
  collectionFile.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations[relation.ID] = relation;
  });
  const entities: Structs.Collection["Entities"] = {};
  const entityFiles: { [key: string]: Structs.EntityDense } = {};
  collectionFile.Entities.forEach((entityID) => {
    const [entity, entityFile] = readEntityPass1(dataBasePath, entityID);
    entities[entity.ID] = entity;
    entityFiles[entityFile.ID] = entityFile;
  });

  const res: Structs.Collection = {
    ID: collectionFile.ID,
    Label: collectionFile.Label,
    Entities: entities,
    Relations: relations,
  };

  collectionFile.Entities.forEach((entityID) => {
    const entity = readEntityPass2(
      entityFiles[entityID],
      (entityID) => {
        return res.Entities[entityID];
      },
      (relationID) => {
        return res.Relations[relationID];
      }
    );
    entities[entity.ID] = entity;
  });

  //console.log(res);
  return res;
}

export function readCollection(
  collectionID: Structs.Collection["ID"],
  dataBasePath: string
): Structs.Collection {
  const collectionFile: Structs.CollectionDense = JSON.parse(
    fs
      .readFileSync(
        path.join(
          dataBasePath,
          "Collections",
          collectionID + ".collection.json"
        )
      )
      .toString()
  );
  console.log(collectionFile);
  /*
  const collection: Structs.Collection = mapCollectionFromFile(
    collectionFile,
    dataBasePath
  );*/
  const collection: Structs.Collection = Collection.expandCondensedCollection(
    collectionFile,
    dataBasePath,
    readRelation,
    readEntityPass1,
    readEntityPass2
  );
  return collection;
}
