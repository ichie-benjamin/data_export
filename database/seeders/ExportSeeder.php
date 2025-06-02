<?php
namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

class ExportSeeder extends Seeder
{
    public function run(): void
    {
        // assumes cleaned JSON files stored in storage/app/cleaned_data
        $files = Storage::disk('local')->files('cleaned_data');
        foreach ($files as $file) {
            $json = json_decode(Storage::disk('local')->get($file), true);
            DB::table('exports')->insert($json);
        }
    }
}
