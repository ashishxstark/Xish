import * as FileSystem from 'expo-file-system';

export async function exportAsJSON(filename: string, data: unknown) {
  const json = JSON.stringify(data, null, 2);
  const path = `${FileSystem.documentDirectory}${filename}.json`;
  await FileSystem.writeAsStringAsync(path, json);
  return path;
}
