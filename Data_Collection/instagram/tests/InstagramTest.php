<?php

require '../vendor/autoload.php';

use InstagramScraper\Instagram;
use InstagramScraper\Model\Media;
use PHPUnit\Framework\TestCase;


class InstagramTest extends TestCase
{
    public function testGetAccountByUsername()
    {
        $account = Instagram::getAccount('kevin');
        $this->assertEquals('kevin', $account->username);
        $this->assertEquals('3', $account->id);
    }

    public function testGetAccountById()
    {
        $account = Instagram::getAccountById(3);
        $this->assertEquals('kevin', $account->username);
        $this->assertEquals('3', $account->id);
    }

    public function testGetMedias()
    {
        $medias = Instagram::getMedias('kevin', 80);
        $this->assertEquals(80, sizeof($medias));
    }

    public function testGet1000Medias()
    {
        $medias = Instagram::getMedias('kevin', 1000);
        $this->assertEquals(1000, sizeof($medias));
    }

    public function testGetMediaByCode()
    {
        $media = Instagram::getMediaByCode('BHaRdodBouH');
        $this->assertEquals('kevin', $media->owner->username);
    }

    public function testGetMediaByUrl()
    {
        $media = Instagram::getMediaByUrl('https://www.instagram.com/p/BHaRdodBouH');
        $this->assertEquals('kevin', $media->owner->username);
    }

    public function testGetLocationTopMediasById()
    {
        $medias = Instagram::getLocationTopMediasById(1);
        $this->assertEquals(9, count($medias));
    }

    public function testGetLocationMediasById()
    {
        $medias = Instagram::getLocationMediasById(1);
        $this->assertEquals(12, count($medias));
    }

    public function testGetLocationById()
    {
        $location = Instagram::getLocationById(1);
        $this->assertEquals('Dog Patch Labs', $location->name);
    }

    public function testGetIdFromCode()
    {
        $code = Media::getCodeFromId('1270593720437182847');
        $this->assertEquals('BGiDkHAgBF_', $code);
        $code = Media::getCodeFromId('1270593720437182847_3');
        $this->assertEquals('BGiDkHAgBF_', $code);
        $code = Media::getCodeFromId(1270593720437182847);
        $this->assertEquals('BGiDkHAgBF_', $code);
    }

    public function testGetCodeFromId()
    {
        $id = Media::getIdFromCode('BGiDkHAgBF_');
        $this->assertEquals(1270593720437182847, $id);
    }
}