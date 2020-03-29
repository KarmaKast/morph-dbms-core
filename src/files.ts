import * as Structs from "./structs";
import * as fs from "fs";
import * as path from "path";

export async function initDatabase(dataBasePath: string): Promise<void> {
  await fs.mkdir(dataBasePath, { recursive: true }, (err) => {
    if (err) {
      console.log(err);
    } else {
      fs.mkdirSync(path.join(dataBasePath, "Entities"), { recursive: true });
      fs.mkdirSync(path.join(dataBasePath, "Collections"), { recursive: true });
      fs.mkdirSync(path.join(dataBasePath, "Relations"), { recursive: true });
      return new Promise((resolve) => {
        resolve();
      });
    }
  });
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(path.join(dataBasePath, "Entities", entity.ID + ".entity")),
    JSON.stringify(entity),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
}

export function writeCollection(
  collection: Structs.Collection,
  dataBasePath: string
): void {
  for (const entityID in collection.Entities) {
    writeEntity(collection.Entities[entityID], dataBasePath);
  }
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Collections", collection.ID + ".collection")
    ),
    JSON.stringify(collection),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
}
