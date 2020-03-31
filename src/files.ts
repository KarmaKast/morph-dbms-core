import * as Structs from "./structs";
import * as fs from "fs";
import * as path from "path";

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
    JSON.stringify(entity),
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
): Structs.CollectionFile {
  const res: Structs.CollectionFile = {
    ID: collection.ID,
    Label: collection.Label,
    Entities: Object.keys(collection.Entities).map((key) => {
      return collection.Entities[key].ID;
    }),
    Relations: Array.from(collection.Relations.values()).map((relation) => {
      return relation.ID;
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
    JSON.stringify(mapCollectionToFile(collection)),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
  for (const entityID in collection.Entities) {
    writeEntity(collection.Entities[entityID], dataBasePath);
  }
  for (const relation of collection.Relations) {
    writeRelation(relation, dataBasePath);
  }
}

// doing: reading from file

export function readEntity(
  entityID: Structs.Entity["ID"],
  dataBasePath: string
): Structs.Entity {
  const entity: Structs.Entity = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Entities", entityID + ".entity.json")
      )
      .toString()
  );
  return entity;
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
  collectionFile: Structs.CollectionFile,
  dataBasePath: string
): Structs.Collection {
  const entities: Structs.Collection["Entities"] = {};
  collectionFile.Entities.forEach((entityID) => {
    const entity = readEntity(entityID, dataBasePath);
    entities[entity.ID] = entity;
  });
  const relations: Structs.Collection["Relations"] = new Set();
  collectionFile.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations.add(relation);
  });

  const res: Structs.Collection = {
    ID: collectionFile.ID,
    Label: collectionFile.Label,
    Entities: entities,
    Relations: relations,
  };
  //console.log(res);
  return res;
}

export function readCollection(
  collectionID: Structs.Collection["ID"],
  dataBasePath: string
): Structs.Collection {
  const collectionFile: Structs.CollectionFile = JSON.parse(
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
  const collection: Structs.Collection = mapCollectionFromFile(
    collectionFile,
    dataBasePath
  );
  return collection;
}
