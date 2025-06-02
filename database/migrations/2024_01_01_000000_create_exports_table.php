<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('exports', function (Blueprint $table) {
            $table->id();
            $table->string('hs');
            $table->string('sitc')->nullable();
            $table->string('country')->nullable();
            $table->text('description');
            $table->unsignedBigInteger('exports_usd')->nullable();
            $table->unsignedBigInteger('quantity')->nullable();
            $table->string('affected')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('exports');
    }
};
