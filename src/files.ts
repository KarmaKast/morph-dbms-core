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

function mapEntityToFile(entity: Structs.Entity): Structs.EntityFile {
  const res: Structs.EntityFile = {
    ID: entity.ID,
    Label: entity.Label,
    RelationClaims: Array.from(entity.RelationClaims.values()).map(
      (RelationClaim) => {
        return {
          To: RelationClaim.To.ID,
          Direction: RelationClaim.Direction,
          Relation: RelationClaim.Relation.ID,
        };
      }
    ),
  };
  if (entity.Data !== undefined) {
    res.Data = entity.Data;
  }
  //console.log(res);
  return res;
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Entities", entity.ID + ".entity.json")
    ),
    JSON.stringify(mapEntityToFile(entity)),
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
  for (const relationID in collection.Relations) {
    writeRelation(collection.Relations[relationID], dataBasePath);
  }
}

// doing: reading from file

function mapEntityFromFile(entityFile: Structs.EntityFile): Structs.Entity {
  const res: Structs.Entity = {
    ID: entityFile.ID,
    Label: entityFile.Label,
    RelationClaims: new Set(),
  };
  if (entityFile.Data !== undefined) {
    res.Data = entityFile.Data;
  }
  return res;

  //console.log(res);
}

export function readEntityPass1(
  dataBasePath: string,
  entityID: Structs.Entity["ID"]
): [Structs.Entity, Structs.EntityFile] {
  const resEntityFile: Structs.EntityFile = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Entities", entityID + ".entity.json")
      )
      .toString()
  );
  const resEntity: Structs.Entity = mapEntityFromFile(resEntityFile);
  return [resEntity, resEntityFile];
}

export function readEntityPass2(
  entityFile: Structs.EntityFile,
  collection: Structs.Collection
): Structs.Entity {
  const resEntity: Structs.Entity = collection.Entities[entityFile.ID];
  entityFile.RelationClaims.forEach((relationClaim) => {
    resEntity.RelationClaims.add({
      To: collection.Entities[relationClaim.To],
      Direction: relationClaim.Direction,
      Relation: collection.Relations[relationClaim.Relation],
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
  collectionFile: Structs.CollectionFile,
  dataBasePath: string
): Structs.Collection {
  const relations: Structs.Collection["Relations"] = {};
  collectionFile.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations[relation.ID] = relation;
  });
  const entities: Structs.Collection["Entities"] = {};
  const entityFiles: { [key: string]: Structs.EntityFile } = {};
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
    const entity = readEntityPass2(entityFiles[entityID], res);
    entities[entity.ID] = entity;
  });

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
