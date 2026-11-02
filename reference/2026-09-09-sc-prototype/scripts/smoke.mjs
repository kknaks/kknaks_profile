import { checkPlace, closePlaceBrowser } from '../server/place.mjs';
try {
  const result = await checkPlace('강남역성형외과', '무이성형외과');
  const { rows, ...summary } = result;
  console.log(JSON.stringify(summary, null, 2));
  if (result.status !== 'found') process.exitCode = 1;
} finally { await closePlaceBrowser(); }
